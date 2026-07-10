from langchain_core.messages import HumanMessage, SystemMessage

from prompts.mermaid_prompt import MERMAID_SYSTEM_PROMPT
from services.openrouter import get_llm
from utils.parser import clean_markdown, normalize_mermaid

def generate_mermaid(flow_description: str) -> str:
    """
    Generates Mermaid Flowchart.
    """

    llm = get_llm()

    response = llm.invoke(
        [
            SystemMessage(
                content=MERMAID_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=flow_description
            ),
        ]
    )

    return normalize_mermaid(clean_markdown(response.content))