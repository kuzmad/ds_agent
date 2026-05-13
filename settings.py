from pydantic_settings import BaseSettings
from pathlib import Path

ROOT_DIR = Path(__file__).parent

class Settings(BaseSettings):
    openai_api_key: str

    proxy_base_url: str = "https://openai.api.proxyapi.ru/v1"
    default_model: str = "openai/gpt-5.4-nano"

    model_config = {"env_file": str(ROOT_DIR / ".env")}
