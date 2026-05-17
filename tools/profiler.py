import pandas as pd
from pathlib import Path
from typing import TypedDict, List, Dict, Any

class ProfileResult(TypedDict):
    shape: tuple
    columns: List[str]
    dtypes: Dict[str, str]
    na_stat: Dict[str, int]
    head: List[Dict[str, Any]]

def read_file(file_path: str) -> pd.DataFrame:
    """
    Читает CSV или Parquet файл и возвращает pandas DataFrame.

    Параметры:
    file_path (str или Path): путь к файлу.

    Возвращает:
    pd.DataFrame: прочитанные данные.

    Исключения:
    ValueError: если расширение файла не поддерживается.
    FileNotFoundError: если файл не существует.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == '.csv':
        return pd.read_csv(path)
    elif suffix == '.parquet':
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}. Ожидается .csv или .parquet")

def profile_dataframe(file_path: str,  n_head: int = 3) -> ProfileResult:
    df = read_file(file_path)
    result_dict = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "na_stat": (df.isna().sum(axis=0) / df.shape[0]).to_dict(),
        "head": df.head(n_head).to_dict(orient="records")
    }
    return result_dict

