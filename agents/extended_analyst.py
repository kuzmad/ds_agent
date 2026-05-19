from pydantic import BaseModel, Field
from graph.agent_state import AgentState
from llm import llm
from langchain_core.prompts import ChatPromptTemplate
from graph.models import ExtendedAnalysis

extended_analyst = ChatPromptTemplate.from_messages([
        ("system", 
     """
    Ты аналитик Data Science, твоя задача на основе переданной аналитики сформировать следующие списки:

    1. id_columns
    2. date_string_columns
    3. high_missing_columns
    4. categorical_columns

    ВАЖНО: ничего не придумывай, используй только информацию из профиля данных. Если пункт не подходит
    ни к одной из категорий - игнорируй его.
    """),
    ("system", 
    """
         Профиль данных: {data_issues}
     """)
]
) | llm.with_structured_output(ExtendedAnalysis)

def extended_analyst_node(state: AgentState) -> dict:
    result = extended_analyst.invoke({"data_issues": state['analysis_result'].data_issues})
    return {
        "extended_analysis": result
    }