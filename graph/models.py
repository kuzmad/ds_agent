from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

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
    date_string_columns: list[str] = Field(description="Список колонок, которые являтся датами, но хранятся в формате str")
    high_missing_columns: Optional[list[str]] = Field(description="Список колонок с высокой долей пропусков выше 90%")
    categorical_columns: list[str] = Field(description="Список колонок, которые являются категориальными переменными")

class TargetConfirmation(BaseModel):
    confirmed: bool = Field(description="Пользователь согласился с текущим значением")
    value: str = Field(description="Итоговое значение — либо текущее, либо новое от пользователя")

class IdColumnsConfirmation(BaseModel):
    confirmed: bool = Field(description="Пользователь согласился с текущим списком")
    value: list[str] = Field(description="Итоговый список колонок")