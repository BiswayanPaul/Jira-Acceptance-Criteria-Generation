from langchain_core.tools import tool

from services.mermaid_service import generate_mermaid


@tool
def generate_mermaid_diagram(flow_description: str) -> str:
    """
    Generate Mermaid Flow Diagram.
    """

    return generate_mermaid(flow_description)