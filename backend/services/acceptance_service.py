from langchain_core.messages import HumanMessage, SystemMessage

from prompts.acceptance_prompt import ACCEPTANCE_SYSTEM_PROMPT
from services.openrouter import get_llm


def generate_acceptance(user_story: str) -> str:
    """
    Generates professional Jira Acceptance Criteria.
    """

    llm = get_llm()

    response = llm.invoke(
        [
            SystemMessage(
                content=ACCEPTANCE_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=user_story
            ),
        ]
    )

    return response.content