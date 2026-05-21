from graph.agent_state import AgentState
from tools.profiler import profile_dataframe, compute_correlation
from llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from graph.models import AnalysisResult

analyst = ChatPromptTemplate.from_messages([
        ("system", 
     """
    Ты аналитик Data Science, твоя задача понять задачу, которую
    необходимо решить из описания пользователя и проанализировать датасет
    на основе предоставленных статистик.

    1. Определи task_type - тип рещаемой задачи, может принимать значения 'classification', 'regression'
    2. Определи target_column - колонка, которую нужно предсказывать. Нужно найти в описании задачи, этот вариант самый приоритетный.
    Если нет в описании, то найти поле 'target' в списке колонок. В противном случае ничего не вернуть.
    3. Определи problem_description - 2-3 предложения, описывающих решаемую задачу и предоставленные данные
    4. Определи data_issues - список найденны проблем (пропуски в данных более чем в 90% случаев, типы переменных, вероятные колонки-идентификаторы)

    ВАЖНО: ничего не придумывай, используй имена колонок из предоставленного profile
    """),
    ("system", 
    """
         Профиль данных:
         - shape: {{ profile.shape }}
         - columns: {{ profile.columns | join(', ') }}
         - dtypes: {{ profile.dtypes }}
         - na_stat: {{ profile.na_stat }}
         - head: {{ profile.head }}
     """),
    ("human", "Описание от пользователя: {query}")
],
template_format="jinja2"
) | llm.with_structured_output(AnalysisResult)

def analyst_node(state: AgentState) -> dict:
    messages = state["messages"]
    last_message = messages[-1].content
    profile = profile_dataframe(state["file_path"])
    result = analyst.invoke({"profile": profile, "query": last_message})
    correlation_matrix = compute_correlation(state["file_path"])
    return {
        "messages": [AIMessage(content=result.problem_description)],
        "analysis_result": result,
        "df_columns": profile["columns"],
        "correlation_matrix": correlation_matrix
    }