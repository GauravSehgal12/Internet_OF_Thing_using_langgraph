import json

from langchain_core.messages import HumanMessage, SystemMessage

from backend.get_llm import get_llm
from backend.prompts import SYSTEM_PROMPT


llm = get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def understand(state):

    messages: list = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    if state.get("messages"):
        messages.extend(state["messages"])

    messages.append(
        HumanMessage(content=state["command"])
    )

    response = llm.invoke(messages)

    content = response.content

    if isinstance(content, list):
        content = "".join(map(str, content))

    content = content.strip()

    if content.startswith("```"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    data = json.loads(content)

    return {

        "messages": [
            HumanMessage(content=state["command"]),
            response
        ],

        "intent": data.get("intent", ""),

        "room": data.get("room", ""),

        "device": data.get("device", ""),

        "action": data.get("action", ""),

        "requires_clarification": data.get(
            "requires_clarification",
            False
        ),

        "clarification_question": data.get(
            "clarification_question",
            ""
        )
    }