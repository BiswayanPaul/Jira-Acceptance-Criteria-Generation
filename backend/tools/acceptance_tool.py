from langchain_core.tools import tool

from services.acceptance_service import generate_acceptance


@tool
def generate_acceptance_criteria(user_story: str) -> str:
    """
    Generate Acceptance Criteria for a Jira Story.
    """

    return generate_acceptance(user_story)