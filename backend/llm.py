import ollama
from prompts import SYSTEM_PROMPT


def generate_acceptance_criteria(story: str):

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": story
            }
        ]
    )

    return response["message"]["content"]