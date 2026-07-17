from backend.graph import graph

config = {
    "configurable": {
        "thread_id": "gaurav"
    }
}

# First command
result = graph.invoke(
    {
        "messages": [],
        "command": "Turn on bedroom light"
    },
    config=config
)

print(result["response"])

# Second command
result = graph.invoke(
    {
        "messages": [],
        "command": "Is the bedroom light on?"
    },
    config=config
)

print(result["response"])