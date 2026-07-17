from typing import TypedDict


class AmbientState(TypedDict):
    command: str

    room: str
    device: str

    action: str

    status: str

    response: str