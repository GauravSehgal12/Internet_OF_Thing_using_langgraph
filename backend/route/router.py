def route(state):

    if state["requires_clarification"]:
        return "clarify"

    return "execute"