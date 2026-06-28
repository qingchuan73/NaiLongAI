"""NaiLongAI 后端入口。

提供基础的健康检查接口与基于 LangChain + 硅基流动 SiliconFlow 的对话接口。
"""
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from chat import chat as llm_chat
from config import settings
from schemas import ChatMessage, ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(
    title="NaiLongAI Backend",
    description="NaiLongAI 后端服务（基于 LangChain + SiliconFlow）",
    version="0.3.0",
)


def _build_messages(req: ChatRequest) -> list:
    """将请求转换为 LangChain 消息列表。

    - 多轮模式（提供 messages）：若不含 system 角色，自动前置默认 system prompt。
    - 单轮模式（仅提供 message）：自动附加 system prompt + 当前用户消息。
    """
    if req.messages:
        lc_messages: list = []
        if not any(m.role == "system" for m in req.messages):
            lc_messages.append(SystemMessage(content=settings.siliconflow_system_prompt))
        for m in req.messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                lc_messages.append(AIMessage(content=m.content))
            else:
                lc_messages.append(SystemMessage(content=m.content))
        return lc_messages

    if req.message:
        return [
            SystemMessage(content=settings.siliconflow_system_prompt),
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
        "model": settings.siliconflow_model,
    }


@app.get("/config")
async def get_config():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "model": settings.siliconflow_model,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """聊天接口（一次性返回完整结果）。"""
    messages = _build_messages(req)

    try:
        content = llm_chat(messages)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用模型失败: {e}")

    return ChatResponse(content=content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)