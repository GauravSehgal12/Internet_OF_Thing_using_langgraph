from langgraph.graph import (
    StateGraph,
    START,
    END
)

from backend.short_memory import memory
from backend.state import AmbientState

from backend.Nodes.understand import understand
from backend.Nodes.execute import execute
from backend.Nodes.clarify import clarify

from backend.route.router import route


builder = StateGraph(AmbientState)

builder.add_node(
    "understand",
    understand
)

builder.add_node(
    "execute",
    execute
)

builder.add_node(
    "clarify",
    clarify
)

builder.add_edge(
    START,
    "understand"
)

builder.add_conditional_edges(

    "understand",

    route,

    {

        "execute": "execute",

        "clarify": "clarify"

    }

)

builder.add_edge(

    "execute",

    END

)

builder.add_edge(

    "clarify",

    END

)

graph = builder.compile(

    checkpointer=memory

)