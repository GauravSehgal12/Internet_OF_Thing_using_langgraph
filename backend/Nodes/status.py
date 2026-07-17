from langchain_core.messages import AIMessage

from backend.device import get_device_status


def status(state):

    room = state.get("room")
    device = state.get("device")

    if device.lower() == "light":
        device_name = f"{room} Light"

    else:
        device_name = f"{room} {device}"

    current_status = get_device_status(device_name)

    response = f"{device_name} is currently {current_status}."

    return {

        "messages": [
            AIMessage(content=response)
        ],

        "response": response

    }