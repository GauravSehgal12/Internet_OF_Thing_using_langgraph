from backend.device import update_device


def execute(state):

    room = state["room"]

    device = state["device"]

    action = state["action"]

    if device.lower() == "light":
        device_name = f"{room} Light"
    else:
        device_name = device

    if action == "turn_on":
        status = "ON"

    elif action == "turn_off":
        status = "OFF"

    elif action == "lock":
        status = "Locked"

    elif action == "unlock":
        status = "Unlocked"

    else:
        return {
            "response": "Unsupported action."
        }

    update_device(
        device_name,
        status
    )

    return {
        "response":
            f"{device_name} has been set to {status}."
    }