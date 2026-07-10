from graph.state import JiraState
from langchain_core.messages import AIMessage

def route_initial(state: JiraState):
    """
    Determines if this is the first turn or a follow-up adjustment request.
    """
    # Check if an assistant message already exists in the conversation history
    has_ai_response = any(isinstance(msg, AIMessage) or msg.type == "ai" for msg in state["messages"])
    
    if state.get("initial_generation_done") or has_ai_response:
        return "chatbot"
    
    return "initial_generation"