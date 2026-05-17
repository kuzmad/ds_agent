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