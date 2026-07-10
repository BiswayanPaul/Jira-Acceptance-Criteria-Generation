import json
from fastapi import FastAPI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from graph.graph import graph
from utils.parser import extract_mermaid
from schemas.models import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/chat")
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    # Restructure standard Pydantic request lists into LangChain structures
    langchain_messages = []
    for msg in request.messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif msg.role in ["assistant", "ai"]:
            langchain_messages.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            langchain_messages.append(SystemMessage(content=msg.content))

    # Run the transaction directly through the compiled LangGraph workflow
    inputs = {"messages": langchain_messages}
    output = graph.invoke(inputs)

    # Grab the terminal interaction response line
    final_messages = output.get("messages", [])
    if not final_messages:
        return ChatResponse(response="Sorry, I wasn't able to compile a response.", mermaid=None)

    final_message = final_messages[-1]
    response_text = final_message.content

    # Isolate any updated flowchart configurations
    mermaid_code = output.get("mermaid_diagram")
    if not mermaid_code:
        mermaid_code = extract_mermaid(response_text)

    return ChatResponse(
        response=response_text,
        mermaid=mermaid_code
    )