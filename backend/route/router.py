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
    
    if state["intent"] == "status_query":
        return "status"

    # Unknown intent
    return "clarify"