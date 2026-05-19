from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from graph.models import AnalysisResult, ExtendedAnalysis


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    file_path: str
    analysis_result: Optional[AnalysisResult]
    extended_analysis: Optional[ExtendedAnalysis]
    confirmed_target: Optional[str]
    confirmed_id_columns: Optional[list[str]]
