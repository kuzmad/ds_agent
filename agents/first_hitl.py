from langgraph.types import interrupt
from langchain_core.prompts import ChatPromptTemplate
from graph.agent_state import AgentState
from llm import llm
from graph.models import TargetConfirmation, IdColumnsConfirmation

parse_target_llm = ChatPromptTemplate.from_messages([
    ("system", """
     Пользователь отвечает на вопрос о целевой колонке.
     Текущее значение: {current_value}
     Список колонок: {cols}
     
     Если пользователь согласен — верни confirmed=true и текущее значение.
     Если предлагает другое — верни confirmed=false и новое значение.
     Пользователь может написать название без ковычек, тебе нужно это обработать.
     Используй только названия колонок, не придумывай. Если пользователь назвал несуществующую
     колонку или написал бессмысленный текст,то верни value="" (пустую строку).
     """),
    ("human", "{user_input}")
]) | llm.with_structured_output(TargetConfirmation)

parse_id_cols_llm = ChatPromptTemplate.from_messages([
    ("system", """
     Пользователь отвечает на вопрос о колонках идентификаторах.
     Текущее значение: {current_value}
     Список колонок: {cols}
     
     Если пользователь согласен — верни confirmed=true и текущее значение.
     Если предлагает другое — верни confirmed=false и новое значение.
     Пользователь может написать название без ковычек, тебе нужно это обработать.
     Используй только названия колонок, не придумывай. Если пользователь назвал несуществующую
     колонку или написал бессмысленный текст,то верни value="" (пустую строку).
     """),
    ("human", "{user_input}")
]) | llm.with_structured_output(IdColumnsConfirmation)

def first_hitl_analyst_node(state: AgentState) -> dict:
    
    # Retry loop для таргета
    while True:
        target_answer = interrupt({
            "question": "Подтвердите таргет для обучения",
            "current_value": state["analysis_result"].target_column,
            "hint": "Введите название колонки или 'ok' для подтверждения"
        })

        parsed_target = parse_target_llm.invoke({
            "current_value": state["analysis_result"].target_column,
            "cols": state["df_columns"],
            "user_input": target_answer
        })

        if parsed_target.value and parsed_target.value in state["df_columns"]:
            break
        
        # value == None значит LLM не нашла колонку — спрашиваем снова
        interrupt({
            "question": "Колонка не найдена в датасете, попробуйте снова",
            "current_value": state["analysis_result"].target_column,
            "available_columns": state["df_columns"]
        })

    while True:
        id_answer = interrupt({
            "question": "Подтвердите колонки-идентификаторы для удаления",
            "current_value": state["extended_analysis"].id_columns,
            "hint": "Введите список через запятую или 'ok' для подтверждения"
        })

        parsed_ids = parse_id_cols_llm.invoke({
            "current_value": state["extended_analysis"].id_columns,
            "cols": state["df_columns"],
            "user_input": id_answer
        })

        if parsed_ids.value and all(col in state["df_columns"] for col in parsed_ids.value):
            break

        interrupt({
            "question": "Некоторые колонки не найдены, попробуйте снова",
            "current_value": state["extended_analysis"].id_columns,
            "available_columns": state["df_columns"]
        })

    return {
        "confirmed_target": parsed_target.value,
        "confirmed_id_columns": parsed_ids.value
    }