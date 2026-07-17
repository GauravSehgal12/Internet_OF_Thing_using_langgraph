from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

from backend.state import AmbientState
from backend.short_memory import memory
from backend.planner import planner
from backend.executor import executor


# -------------------------
# Build Graph
# -------------------------

builder = StateGraph(AmbientState)

# Nodes
builder.add_node("planner", planner)
builder.add_node("executor", executor)

# Flow
builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", END)

# Compile with Memory
graph = builder.compile(
    checkpointer=memory
)


# -------------------------
# Local Testing
# -------------------------

if __name__ == "__main__":

    # Build a RunnableConfig instance for type correctness
    config = RunnableConfig(configurable={"thread_id": "demo-user"})

    state: AmbientState = {

        "messages": [],

        "command": "Turn on bedroom light",

        "room": "",

        "device": "",

        "action": "",

        "response": ""
    }

    result = graph.invoke(
        state,
        config=config
    )

    print(result)