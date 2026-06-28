"""应用配置（从环境变量加载）。"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 应用基础配置
    app_name: str = "NaiLongAI"
    debug: bool = False
    port: int = 8000

    # DeepSeek 配置
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    deepseek_temperature: float = 0.7
    deepseek_system_prompt: str = "你是一个友好、专业的AI助手，名叫NaiLongAI。请用简洁清晰的中文回答用户的问题。"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()