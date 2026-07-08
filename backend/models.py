from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    temperature: float
    max_tokens: int
    messages: list[Message]