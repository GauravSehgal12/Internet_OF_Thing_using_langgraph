from fastapi import FastAPI
from pydantic import BaseModel

from backend.graph import graph
from backend.device import (
    get_devices,
    reset_devices,
)

app = FastAPI(
    title="Ambient Smart Home Assistant",
    version="1.0"
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def home():
    return {
        "message": "Ambient Smart Home Assistant API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }


@app.get("/devices")
def devices():

    return get_devices()


@app.post("/reset")
def reset():

    reset_devices()

    return {
        "message": "Smart Home Reset Successful"
    }


@app.post("/invoke")
def invoke(req: CommandRequest):

    result = graph.invoke(
        {
            "command": req.command,

            "room": "",

            "device": "",

            "action": "",

            "status": "",

            "response": ""
        }
    )

    return {

        "response": result["response"],

        "room": result["room"],

        "device": result["device"],

        "action": result["action"],

        "status": result["status"],

        "devices": get_devices()
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )