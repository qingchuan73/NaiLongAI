"""LangChain DeepSeek 模型封装。"""
from functools import lru_cache
from typing import Iterator

from langchain_core.messages import BaseMessage
from langchain_deepseek import ChatDeepSeek

from config import settings


@lru_cache
def get_llm() -> ChatDeepSeek:
    """获取（缓存的）ChatDeepSeek 实例。"""
    if not settings.deepseek_api_key or settings.deepseek_api_key == "your-deepseek-api-key":
        raise ValueError(
            "DEEPSEEK_API_KEY 未配置，请在 .env 文件中设置有效的 DeepSeek API Key"
        )

    return ChatDeepSeek(
        model=settings.deepseek_model,
        temperature=settings.deepseek_temperature,
        api_key=settings.deepseek_api_key,
        max_retries=2,
    )


def stream_chat(messages: list[BaseMessage]) -> Iterator[str]:
    """流式调用模型，逐块返回文本内容。"""
    llm = get_llm()
    for chunk in llm.stream(messages):
        if isinstance(chunk.content, str):
            yield chunk.content