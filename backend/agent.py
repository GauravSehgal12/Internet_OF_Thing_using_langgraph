import sys
import os
import json
from typing import List, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.get_llm import get_llm

load_dotenv()

# Initialize LLM once
llm = get_llm(model="llama-3.3-70b-versatile", temperature=0)


class AgentState(TypedDict):
    input: str
    target_temp: int
    current_temp: int
    tool_call: bool
    action: str
    log: List[str]


def smart_thermostat_tool(action: str, temp: int) -> str:
    return f"Smart Thermostat updated: Action={action}, NewTemp={temp}°C"


def react_agent(state: AgentState):
    prompt = f"""
You are a smart thermostat assistant.

Current room temperature: {state['current_temp']}°C

User command:
{state['input']}

Respond ONLY with valid JSON.

Example:
{{
    "tool_call": true,
    "action": "heat",
    "temp": 24
}}
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            x.get("text", "") if isinstance(x, dict) else str(x)
            for x in content
        )

    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(content)

        return {
            "tool_call": data["tool_call"],
            "action": data["action"],
            "target_temp": data["temp"],
            "log": state["log"]
            + [
                f"Agent Decision -> Tool={data['tool_call']}, Action={data['action']}, Temp={data['temp']}"
            ],
        }

    except Exception as e:
        return {
            "tool_call": False,
            "action": "",
            "target_temp": state["current_temp"],
            "log": state["log"] + [f"JSON Parsing Error: {e}"],
        }


def tool_executor(state: AgentState):
    result = smart_thermostat_tool(
        state["action"],
        state["target_temp"],
    )

    return {
        "current_temp": state["target_temp"],
        "log": state["log"] + [result],
    }


def router(state: AgentState):
    if state["tool_call"]:
        return "tools"
    return END


builder = StateGraph(AgentState)

builder.add_node("agent", react_agent)
builder.add_node("tools", tool_executor)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    router,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", END)

graph = builder.compile()


if __name__ == "__main__":

    print("====== Smart Thermostat Agent ======")

    initial_state: AgentState = {
        "input": "Make the room warmer. Set to 24 degrees.",
        "target_temp": 0,
        "current_temp": 19,
        "tool_call": False,
        "action": "",
        "log": [],
    }

    result = graph.invoke(initial_state)

    print("\nExecution Log\n")

    for item in result["log"]:
        print(item)

    print("\nFinal Temperature:", result["current_temp"])