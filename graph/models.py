from pydantic import BaseModel, Field
from enum import Enum

class TaskType(str, Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"

class AnalysisResult(BaseModel):
    task_type: TaskType = Field(description="Тип решаемой задачи для разработки модели")
    target_column: str = Field(description="Поле, которое в датафрейме отвечает за target - предсказываемое значение")
    problem_description: str = Field(description="Общее резюме решаемой задачи и имеющихся данных")
    data_issues: list[str] = Field(description="Описание найденных проблем в данных: пропуски, выбросы и т.д.")

class ExtendedAnalysis(BaseModel):
    id_columns: list[str] = Field(description="Список колонок, которые потенциально являются идентификаторами")
    date_string: list[str] = Field(description="Список колонок, которые являтся датами, но хранятся в формате str")
    high_missing_columns: dict = Field(description="Список колонок с высоким порогом")
    categorica_columns: list[str] = Field(description="Список колонок, которые являются категориальными переменными")