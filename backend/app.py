from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from backend.graph import graph
from backend.device import (
    get_devices,
    reset_devices,
)

app = FastAPI(
    title="Smart Home Assistant",
    version="1.0.0"
)


# ----------------------------
# Request / Response Models
# ----------------------------

class ChatRequest(BaseModel):
    thread_id: str
    command: str


class ChatResponse(BaseModel):
    response: str
    devices: Dict[str, str]


# ----------------------------
# Chat Endpoint
# ----------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = graph.invoke(
        {
            "messages": [],
            "command": request.command
        },
        config=config
    )

    return ChatResponse(
        response=result["response"],
        devices=get_devices()
    )


# ----------------------------
# Get All Devices
# ----------------------------

@app.get("/devices")
def devices():

    return get_devices()


# ----------------------------
# Reset Devices
# ----------------------------

@app.post("/reset")
def reset():

    reset_devices()

    return {
        "message": "All devices have been reset successfully.",
        "devices": get_devices()
    }