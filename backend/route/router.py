def route(state):

    # Missing information
    if state["requires_clarification"]:
        return "clarify"

    # Status queries
    if state["intent"] == "status_query":
        return "status"

    # Device control
    if state["intent"] == "device_control":
        return "execute"

    # Unknown intent
    return "clarify"