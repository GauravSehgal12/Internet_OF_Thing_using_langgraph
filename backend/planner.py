import json

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from backend.get_llm import get_llm
from backend.prompts import SYSTEM_PROMPT

llm = get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0,
)


def planner(state):

    messages = []

    # System Prompt
    messages.append(
        SystemMessage(content=SYSTEM_PROMPT)
    )

    # Previous conversation
    if state.get("messages"):
        messages.extend(state["messages"])

    # Current command
    messages.append(
        HumanMessage(
            content=state["command"]
        )
    )

    response = llm.invoke(messages)

    content = response.content

    result = {}

    # Remove markdown if present
    if isinstance(content, str):
        content = content.strip()

        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        try:
            result = json.loads(content)
        except Exception:
            result = {}

    if not isinstance(result, dict):
        result = {}

    return {

        "messages": [
            HumanMessage(content=state["command"]),
            response,
        ],

        "room": result.get("room", ""),

        "device": result.get("device", ""),

        "action": result.get("action", ""),
    }