import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "poolside/laguna-xs-2.1:free"
)

DEFAULT_TEMPERATURE = float(
    os.getenv(
        "DEFAULT_TEMPERATURE",
        0.5
    )
)

DEFAULT_MAX_TOKENS = int(
    os.getenv(
        "DEFAULT_MAX_TOKENS",
        1024
    )
)

# Safety cap on the agent's tool-calling loop (model -> tool -> model -> ...)
# Prevents an infinite loop if the model keeps requesting tools.
MAX_TOOL_ITERATIONS = int(
    os.getenv(
        "MAX_TOOL_ITERATIONS",
        5
    )
)