from langchain_core.messages import AIMessage


def clarify(state):

    question = state.get(
        "clarification_question",
        "Can you clarify your request?"
    )

    return {

        "messages": [
            AIMessage(content=question)
        ],

        "response": question

    }