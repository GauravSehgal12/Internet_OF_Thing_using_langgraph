import json

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from backend.get_llm import get_llm
from backend.prompts import SYSTEM_PROMPT


llm = get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def understand(state):

    # Build conversation
    conversation: list[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    # Previous conversation
    if state.get("messages"):
        conversation.extend(state["messages"])

    # Current user command
    conversation.append(
        HumanMessage(content=state["command"])
    )

    try:

        response = llm.invoke(conversation)

        content = response.content

        if isinstance(content, list):
            content = "".join(map(str, content))

        content = content.strip()

        # Remove markdown if the LLM returns ```json ... ```
        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(content)

        # Human-readable summary for conversation memory
        if data.get("requires_clarification", False):
            summary = data.get(
                "clarification_question",
                "I need a little more information."
            )
        else:
            summary = (
                f"I understood that you want to "
                f"{data.get('action', '').replace('_', ' ')} "
                f"the {data.get('room', '')} "
                f"{data.get('device', '')}."
            )

    except Exception as e:

        print("Understand Node Error:", e)

        summary = "Sorry, I couldn't understand your request."

        return {

            "messages": [

                HumanMessage(
                    content=state["command"]
                ),

                AIMessage(
                    content=summary
                )

            ],

            "intent": "",

            "room": "",

            "device": "",

            "action": "",

            "requires_clarification": True,

            "clarification_question": "Can you rephrase your request?"
        }

    return {

        "messages": [

            HumanMessage(
                content=state["command"]
            ),

            AIMessage(
                content=summary
            )

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