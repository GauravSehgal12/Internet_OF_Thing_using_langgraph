import json

from langgraph.graph import StateGraph, START, END

from backend.get_llm import get_llm
from backend.state import AmbientState
from backend.prompts import SYSTEM_PROMPT
from backend.device import DEVICE_STATUS


llm = get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def planner(state: AmbientState):

    prompt = f"""
{SYSTEM_PROMPT}

User Command:

{state["command"]}
"""

    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        content = "\n".join(
            item if isinstance(item, str) else json.dumps(item)
            for item in content
        )
    else:
        content = str(content)
    content = content.strip()

    if content.startswith("```"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    data = json.loads(content)

    return {

        "room": data["room"],

        "device": data["device"],

        "action": data["action"],

        "status": data["status"],

        "response": data["response"]
    }


def executor(state: AmbientState):

    device_name = f"{state['room']} {state['device']}"

    if device_name in DEVICE_STATUS:

        DEVICE_STATUS[device_name] = state["status"]

    elif state["device"] == "Fan":

        DEVICE_STATUS["Fan"] = state["status"]

    elif state["device"] == "AC":

        DEVICE_STATUS["AC"] = state["status"]

    elif state["device"] == "Door":

        DEVICE_STATUS["Door"] = state["status"]

    return {}


builder = StateGraph(AmbientState)

builder.add_node("planner", planner)

builder.add_node("executor", executor)

builder.add_edge(START, "planner")

builder.add_edge("planner", "executor")

builder.add_edge("executor", END)

graph = builder.compile()