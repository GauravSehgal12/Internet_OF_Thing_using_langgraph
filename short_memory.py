import os
import sys
from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import HumanMessage, AIMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.get_llm import get_llm

load_dotenv()


# -----------------------------
# State
# -----------------------------
class MemoryState(TypedDict):
    messages: Annotated[list, add_messages]


# -----------------------------
# Chat Node
# -----------------------------
def chat_node(state: MemoryState):
    llm = get_llm(
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    system_prompt = HumanMessage(
        content="You are a helpful home assistant."
    )

    # Send previous conversation + current message
    response = llm.invoke([system_prompt] + state["messages"])

    return {
        "messages": [
            AIMessage(content=response.content)
        ]
    }


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(MemoryState)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    print("------ LangGraph Short-Term Memory ------")

    try:
        print(graph.get_graph().draw_ascii())
    except Exception:
        pass

    config = {
        "configurable": {
            "thread_id": "chat-session-45"
        }
    }

    # ---------------- Turn 1 ----------------
    print("\nTurn 1")

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="Hello! I am John.")
            ]
        },
        config=config,
    )

    print("Assistant:", result["messages"][-1].content)

    # ---------------- Turn 2 ----------------
    print("\nTurn 2")

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="What is my name?")
            ]
        },
        config=config,
    )

    print("Assistant:", result["messages"][-1].content)

    # ---------------- Turn 3 ----------------
    print("\nTurn 3")

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="What did I say in my first message?")
            ]
        },
        config=config,
    )

    print("Assistant:", result["messages"][-1].content)