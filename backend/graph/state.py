from typing import Annotated

from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages

from langchain_core.messages import AnyMessage


class JiraState(MessagesState):
    """
    Shared graph state.
    """

    messages: Annotated[list[AnyMessage], add_messages]

    acceptance_criteria: str | None = None

    mermaid_diagram: str | None = None

    initial_generation_done: bool = False