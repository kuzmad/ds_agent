from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    file_path: str
    task_type: Optional[str]
    target_column: Optional[str]
    problem_description: Optional[str]
    data_issues: Optional[list[str]]
