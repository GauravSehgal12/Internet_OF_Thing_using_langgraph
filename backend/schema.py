from pydantic import BaseModel


class IntentSchema(BaseModel):

    intent: str

    room: str

    device: str

    action: str

    requires_clarification: bool

    clarification_question: str