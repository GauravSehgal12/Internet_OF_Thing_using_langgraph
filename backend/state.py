from typing import Annotated, TypedDict

from langgraph.graph import add_messages


class AmbientState(TypedDict):

    messages: Annotated[list, add_messages]

    command: str

    room: str

    device: str

    action: str

    response: str