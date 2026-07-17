from langchain_core.messages import AIMessage

from backend.device import update_device


ACTION_STATUS = {
    "turn_on": "ON",
    "turn_off": "OFF",
    "lock": "Locked",
    "unlock": "Unlocked",
}


def execute(state):

    room = state.get("room")
    device = state.get("device")
    action = state.get("action")

    if not room or not device or not action:

        response = "I don't have enough information to execute that command."

        return {

            "messages": [
                AIMessage(content=response)
            ],

            "response": response

        }

    if device.lower() == "light":
        device_name = f"{room} Light"

    else:
        device_name = f"{room} {device}"

    status = ACTION_STATUS.get(action)

    if status is None:

        response = "Unsupported action."

        return {

            "messages": [
                AIMessage(content=response)
            ],

            "response": response

        }

    update_device(
        device_name,
        status
    )

    response = f"{device_name} has been set to {status}."

    return {

        "messages": [
            AIMessage(content=response)
        ],

        "response": response

    }