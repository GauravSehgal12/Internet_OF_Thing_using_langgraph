import json

from langgraph.graph import StateGraph, START, END

from backend.get_llm import get_llm
from backend.state import AmbientState
from backend.prompts import SYSTEM_PROMPT
from backend.device import update_device


# -----------------------------
# Initialize LLM
# -----------------------------
llm = get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# -----------------------------
# Planner Node
# -----------------------------
def planner(state: AmbientState):

    prompt = f"""
{SYSTEM_PROMPT}

User Command:
{state["command"]}
"""

    response = llm.invoke(prompt)

    content = response.content

    # Handle Groq returning list content
    if isinstance(content, list):
        content = "".join(
            item if isinstance(item, str)
            else str(item)
            for item in content
        )

    content = content.strip()

    # Remove markdown if present
    if content.startswith("```"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:

        data = json.loads(content)

        return {

            "room": data["room"],

            "device": data["device"],

            "action": data["action"],

            "status": data["status"],

            "response": data["response"]
        }

    except Exception:

        return {

            "room": "",

            "device": "",

            "action": "",

            "status": "",

            "response": "Sorry, I could not understand the command."
        }


# -----------------------------
# Executor Node
# -----------------------------
def executor(state: AmbientState):

    room = state["room"]
    device = state["device"]
    status = state["status"]

    # Build full device name
    if device.lower() == "light":

        device_name = f"{room} Light"

    else:

        device_name = device

    # Update simulated device state
    update_device(
        device_name,
        status
    )

    return {}


# -----------------------------
# Build LangGraph
# -----------------------------
builder = StateGraph(AmbientState)

builder.add_node(
    "planner",
    planner
)

builder.add_node(
    "executor",
    executor
)

builder.add_edge(
    START,
    "planner"
)

builder.add_edge(
    "planner",
    "executor"
)

builder.add_edge(
    "executor",
    END
)

graph = builder.compile()


# -----------------------------
# Local Testing
# -----------------------------
if __name__ == "__main__":

    print("====== Ambient Smart Home Agent ======\n")

    initial_state : AmbientState = {

        "command": "Turn on the bedroom light",

        "room": "",

        "device": "",

        "action": "",

        "status": "",

        "response": ""
    }

    result = graph.invoke(initial_state)

    print("LLM Response")
    print("------------------------")

    print(result["response"])

    print()

    print("Room      :", result["room"])
    print("Device    :", result["device"])
    print("Action    :", result["action"])
    print("Status    :", result["status"])