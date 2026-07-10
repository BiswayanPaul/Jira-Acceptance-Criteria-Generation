from langchain_openai import ChatOpenAI

from config import (
    OPENROUTER_API_KEY,
    BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
):
    """
    Returns a LangChain ChatOpenAI client configured to use OpenRouter.
    """

    return ChatOpenAI(
        model=model,
        api_key=OPENROUTER_API_KEY,
        base_url=BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
    )