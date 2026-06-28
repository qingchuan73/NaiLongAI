"""LangChain 硅基流动（SiliconFlow）对话模块。

硅基流动兼容 OpenAI Chat Completions 协议，因此直接复用 `langchain-openai` 的
`ChatOpenAI`，并通过 `base_url` 指向硅基流动的 API 网关即可。

默认模型：deepseek-ai/DeepSeek-V3
"""
from functools import lru_cache

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from config import settings


@lru_cache
def get_llm() -> ChatOpenAI:
    """获取（缓存的）ChatOpenAI 实例，指向硅基流动 API。"""
    if not settings.siliconflow_api_key:
        raise ValueError(
            "SILICONFLOW_API_KEY 未配置，请在 .env 文件中设置有效的硅基流动 API Key"
        )

    return ChatOpenAI(
        model=settings.siliconflow_model,
        base_url=settings.siliconflow_base_url,
        api_key=settings.siliconflow_api_key,
        temperature=settings.siliconflow_temperature,
        max_retries=2,
    )


def chat(messages: list[BaseMessage]) -> str:
    """调用模型进行一次性对话，返回模型回复的纯文本。

    使用示例：
        from langchain_core.messages import SystemMessage, HumanMessage
        reply = chat([
            SystemMessage(content="你是一个有帮助的助手"),
            HumanMessage(content="你好"),
        ])
    """
    llm = get_llm()
    result = llm.invoke(messages)
    return result.content if isinstance(result.content, str) else str(result.content)


if __name__ == "__main__":
    # 本地快速验证：
    #     python chat.py
    from langchain_core.messages import HumanMessage, SystemMessage

    reply = chat(
        [
            SystemMessage(content=settings.siliconflow_system_prompt),
            HumanMessage(content="你好，请用一句话介绍你自己。"),
        ]
    )
    print("AI:", reply)