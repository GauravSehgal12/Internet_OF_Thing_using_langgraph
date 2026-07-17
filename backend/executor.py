from backend.device import update_device


def executor(state):

    room = state["room"]
    device = state["device"]
    action = state["action"]

    # ------------------------
    # Validation
    # ------------------------

    if not room and device == "Light":
        return {
            "response": "Which room's light would you like to control?"
        }

    if not device:
        return {
            "response": "I couldn't determine which device you meant."
        }

    # ------------------------
    # Build Device Name
    # ------------------------

    if device == "Light":
        device_name = f"{room} Light"
    else:
        device_name = device

    # ------------------------
    # Action Logic
    # ------------------------

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

    # ------------------------
    # Update Smart Home
    # ------------------------

    update_device(
        device_name,
        status
    )

    # ------------------------
    # Response
    # ------------------------

    return {

        "response": f"{device_name} has been set to {status}.",

        "status": status
    }