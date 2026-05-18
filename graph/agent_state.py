from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from graph.models import AnalysisResult, ExtendedAnalysis


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    file_path: str
    task_type: Optional[str]
    analysis_result: Optional[AnalysisResult]
    target_column: Optional[str]
    problem_description: Optional[str]
    data_issues: Optional[list[str]]
    extended_analysis: Optional[ExtendedAnalysis]
