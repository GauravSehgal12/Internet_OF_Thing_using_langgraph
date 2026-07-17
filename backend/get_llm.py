import os

from langchain_groq import ChatGroq

# from langchain_groq import ChatGroq
def get_llm(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
):
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY not found. Add it to your .env file."
        )

    try:
        llm = ChatGroq(
            model=model,
            temperature=temperature,
            max_retries=2,
        )

        llm.invoke("Hi")

        print(f"--- Using Groq ({model}) ---")
        return llm

    except Exception as e:
        raise RuntimeError(f"Failed to connect to Groq: {e}")


