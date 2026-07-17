from backend.planner import planner

state = {
    "messages": [],
    "command": "Turn on bedroom light",
}

print(planner(state))