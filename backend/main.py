"""NaiLongAI 后端入口。

提供基础的健康检查接口与基于 LangChain + DeepSeek 的对话接口。
"""
from collections.abc import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage

from chat import get_llm, stream_chat
from config import settings
from schemas import ChatMessage, ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(
    title="NaiLongAI Backend",
    description="NaiLongAI 后端服务（基于 LangChain + DeepSeek）",
    version="0.2.0",
)


def _build_messages(req: ChatRequest) -> list:
    """将请求转换为 LangChain 消息列表。

    - 多轮模式（提供 messages）：若不含 system 角色，自动前置默认 system prompt。
    - 单轮模式（仅提供 message）：自动附加 system prompt + 当前用户消息。
    """
    if req.messages:
        lc_messages = []
        has_system = any(m.role == "system" for m in req.messages)
        if not has_system:
            lc_messages.append(SystemMessage(content=settings.deepseek_system_prompt))
        for m in req.messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                from langchain_core.messages import AIMessage

                lc_messages.append(AIMessage(content=m.content))
            else:
                lc_messages.append(SystemMessage(content=m.content))
        return lc_messages

    if req.message:
        return [
            SystemMessage(content=settings.deepseek_system_prompt),
            HumanMessage(content=req.message),
        ]

    raise HTTPException(
        status_code=422,
        detail="请求必须包含 `message` 或 `messages` 字段之一",
    )


@app.get("/")
async def root():
    return {
        "message": "Hello, NaiLongAI!",
        "app_name": settings.app_name,
        "model": settings.deepseek_model,
    }


@app.get("/config")
async def get_config():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "model": settings.deepseek_model,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """非流式聊天接口。"""
    try:
        messages = _build_messages(req)
    except HTTPException:
        raise

    try:
        llm = get_llm()
        result = llm.invoke(messages)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用模型失败: {e}")

    return ChatResponse(content=result.content if isinstance(result.content, str) else str(result.content))


def _sse_format(data: str) -> str:
    """将字符串按 SSE 协议格式化。"""
    if not data:
        return ""
    escaped = data.replace("\n", "\\n")
    return f"data: {escaped}\n\n"


async def _stream_generator(req: ChatRequest) -> AsyncIterator[bytes]:
    """流式生成器，以 SSE 协议输出。"""
    try:
        messages = _build_messages(req)
    except HTTPException as e:
        yield f"data: [ERROR] {e.detail}\n\n".encode("utf-8")
        return

    try:
        for chunk in stream_chat(messages):
            if chunk:
                yield _sse_format(chunk).encode("utf-8")
        yield _sse_format("[DONE]").encode("utf-8")
    except ValueError as e:
        yield f"data: [ERROR] {e}\n\n".encode("utf-8")
    except Exception as e:
        yield f"data: [ERROR] 调用模型失败: {e}\n\n".encode("utf-8")


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """流式聊天接口（Server-Sent Events）。

    每条消息格式：
        data: <内容片段>\\n\\n
    流结束时发送：
        data: [DONE]\\n\\n
    """
    return StreamingResponse(
        _stream_generator(req),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)