from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class AmbientState(TypedDict):

    messages: Annotated[list, add_messages]

    command: str

    intent: str

    room: str

    device: str

    action: str

    requires_clarification: bool

    clarification_question: str

    response: str