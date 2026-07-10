from services.openrouter import get_llm

from tools.acceptance_tool import generate_acceptance_criteria
from tools.mermaid_tool import generate_mermaid_diagram


TOOLS = [
    generate_acceptance_criteria,
    generate_mermaid_diagram,
]


llm = get_llm()

agent = llm.bind_tools(TOOLS)