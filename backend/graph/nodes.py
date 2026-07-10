from langchain_core.messages import AIMessage, SystemMessage
from graph.state import JiraState
from services.acceptance_service import generate_acceptance
from services.mermaid_service import generate_mermaid
from agents.jira_agent import agent
from prompts.agent_prompt import AGENT_SYSTEM_PROMPT

def initial_generation(state: JiraState):
    """
    Generates the initial batch of acceptance criteria and flowcharts on the first turn.
    """
    story = state["messages"][-1].content

    acceptance = generate_acceptance(story)
    diagram = generate_mermaid(acceptance)

    return {
        "messages": [
            AIMessage(
                content=f"{acceptance}\n\n---\n\n```mermaid\n{diagram}\n```"
            )
        ],
        "acceptance_criteria": acceptance,
        "mermaid_diagram": diagram,
        "initial_generation_done": True
    }

def chatbot(state: JiraState):
    """
    Handles subsequent edits, revisions, and conversational fine-tuning.
    """
    messages = state["messages"]
    
    # Inject the core agent instruction blueprint if it is missing
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + messages

    response = agent.invoke(messages)
    
    return {
        "messages": [response]
    }
    
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from utils.parser import clean_markdown, normalize_mermaid  # normalize_mermaid from earlier fix

def capture_tool_outputs(state: JiraState):
    """
    Runs right after ToolNode executes. Reads the most recent consecutive
    ToolMessages (produced by this turn's tool calls) and writes their
    content directly into state — instead of relying on the LLM to
    faithfully re-forward tool output as clean text later.
    """
    updates = {}
    for msg in reversed(state["messages"]):
        if not isinstance(msg, ToolMessage):
            break  # stop once we're past this turn's batch of tool results
        if msg.name == "generate_mermaid_diagram":
            updates["mermaid_diagram"] = normalize_mermaid(clean_markdown(msg.content))
        elif msg.name == "generate_acceptance_criteria":
            updates["acceptance_criteria"] = clean_markdown(msg.content)
    return updates