from backend.Nodes.understand import understand

state = {

    "messages": [],

    "command": "Turn on bedroom light"

}

result = understand(state)

print(result)