from fastapi import FastAPI

from llm import chat
from models import ChatRequest
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    logger.info(
    f"Model={request.model}"
)

    answer = chat(
        model=request.model,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    return {
        "response": answer
    }
    
@app.get("/health")
def health():
    return {
        "status": "ok"
    }