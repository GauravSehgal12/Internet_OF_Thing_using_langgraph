from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from backend.state import AmbientState
from backend.short_memory import memory

from backend.Nodes.understand import understand
from backend.Nodes.execute import execute
from backend.Nodes.status import status
from backend.Nodes.clarify import clarify

from backend.route.router import route


builder = StateGraph(AmbientState)

# ---------------- Nodes ---------------- #

builder.add_node(
    "understand",
    understand,
)

builder.add_node(
    "execute",
    execute,
)

builder.add_node(
    "status",
    status,
)

builder.add_node(
    "clarify",
    clarify,
)

# ---------------- Flow ---------------- #

builder.add_edge(
    START,
    "understand",
)

builder.add_conditional_edges(
    "understand",
    route,
    {
        "execute": "execute",
        "status": "status",
        "clarify": "clarify",
    },
)

builder.add_edge(
    "execute",
    END,
)

builder.add_edge(
    "status",
    END,
)

builder.add_edge(
    "clarify",
    END,
)

graph = builder.compile(
    checkpointer=memory
)