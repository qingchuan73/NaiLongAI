"""请求/响应数据模型。"""
from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["user", "assistant", "system"]


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    """聊天请求体。

    - 若提供 messages，则按多轮对话处理（不附加 system prompt，避免覆盖已有 system 角色）。
    - 若仅提供 message，则视为单轮对话，自动附加默认 system prompt。
    """

    message: str | None = Field(default=None, description="单轮消息（与 messages 二选一）")
    messages: list[ChatMessage] | None = Field(
        default=None, description="多轮消息历史"
    )
    stream: bool = Field(default=True, description="是否使用流式响应")


class ChatChunk(BaseModel):
    """流式响应的单个 chunk。"""

    content: str
    done: bool = False


class ChatResponse(BaseModel):
    """非流式响应的完整结果。"""

    content: str