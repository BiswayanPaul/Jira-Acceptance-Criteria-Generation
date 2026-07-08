import ollama
from prompts import SYSTEM_PROMPT


def chat(model, messages, temperature, max_tokens):

    ollama_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # If this isn't the first turn, add an extra instruction.
    if len(messages) > 1:
        ollama_messages.append(
            {
                "role": "system",
                "content": (
                    "This is an ongoing conversation.\n"
                    "If the user asks to modify, remove, improve, rewrite, "
                    "or update something, modify the PREVIOUS assistant response "
                    "instead of generating completely new acceptance criteria.\n"
                    "Only change what the user requested."
                )
            }
        )

    for message in messages:
        ollama_messages.append(
            {
                "role": message.role,
                "content": message.content
            }
        )

    response = ollama.chat(
        model=model,
        messages=ollama_messages,
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"]