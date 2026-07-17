from backend.device import update_device


def executor(state):

    room = state.get("room", "")
    device = state.get("device", "")
    action = state.get("action", "")

    if not device:
        return {
            "response": "I couldn't determine which device you meant."
        }

    if device.lower() == "light":

        if not room:
            return {
                "response": "Which room's light would you like to control?"
            }

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

        "response": f"{device_name} has been set to {status}."
    }