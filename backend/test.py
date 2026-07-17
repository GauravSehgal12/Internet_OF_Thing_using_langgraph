from backend.executor import executor

state = {

    "room": "Bedroom",

    "device": "Light",

    "action": "turn_on"

}

print(executor(state))