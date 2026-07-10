from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from graph.state import JiraState
from graph.nodes import chatbot, initial_generation, capture_tool_outputs
from graph.router import route_initial
from agents.jira_agent import TOOLS

# Initialize the state-tracked architecture
builder = StateGraph(JiraState)

# Define structural nodes
builder.add_node("initial_generation", initial_generation)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_node("capture_tool_outputs", capture_tool_outputs)

# Map conditional entry points
builder.add_conditional_edges(
    START,
    route_initial,
    {
        "initial_generation": "initial_generation",
        "chatbot": "chatbot",
    },
)

# Route leaf connections
builder.add_edge("initial_generation", END)

# Configure the agent tool-calling execution loop
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "capture_tool_outputs")
builder.add_edge("capture_tool_outputs", "chatbot")

# Compile the target workflow engine
graph = builder.compile()