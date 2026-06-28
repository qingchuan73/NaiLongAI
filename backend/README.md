# NaiLongAI Backend

基于 FastAPI + LangChain + DeepSeek 构建的 AI 对话后端服务。

## 功能特性

- 🚀 **FastAPI**：高性能异步 Web 框架
- 🔗 **LangChain**：LLM 应用编排框架
- 🤖 **DeepSeek**：高性价比大语言模型（`deepseek-chat`）
- 💬 **流式对话**：基于 Server-Sent Events 的 token 级流式输出
- ⚙️ **配置管理**：通过 `.env` 文件和环境变量管理

## 环境要求

- Python 3.10+
- pip
- DeepSeek API Key（[申请地址](https://platform.deepseek.com)）

## 快速开始

### 1. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，至少填入 DEEPSEEK_API_KEY
```

`.env` 示例：

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.7
```

### 4. 启动服务

```bash
# 方式一：使用 uvicorn（推荐）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式二：使用 fastapi dev（需要 fastapi[standard]）
fastapi dev

# 方式三：直接运行
python main.py
```

## 接口说明

启动后可访问：

| 地址 | 说明 |
| --- | --- |
| http://localhost:8000 | 根路径 |
| http://localhost:8000/docs | Swagger API 文档 |
| http://localhost:8000/redoc | ReDoc API 文档 |

### 1. `GET /` — 根路径

返回应用基本信息。

### 2. `GET /config` — 应用配置

返回当前生效的应用配置。

### 3. `POST /chat` — 单次聊天（非流式）

请求体：

```json
{
  "message": "你好，请介绍下你自己",
  "stream": false
}
```

或使用多轮消息历史：

```json
{
  "messages": [
    {"role": "system", "content": "你是一位诗人"},
    {"role": "user", "content": "写一首关于秋天的诗"}
  ]
}
```

响应：

```json
{
  "content": "AI 的回复内容..."
}
```

### 4. `POST /chat/stream` — 流式聊天（SSE）

请求体同上。

响应为 SSE 流：

```
data: 你
data: 好
data: ！
data: 我
data: 是
...
data: [DONE]
```

可使用 curl 测试：

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

或使用 PowerShell：

```powershell
$body = @{message = "你好"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/chat/stream" `
  -Method POST -ContentType "application/json" -Body $body
```

## 项目结构

```
backend/
├── main.py              # FastAPI 应用入口（路由定义）
├── chat.py              # LangChain 模型封装（流式聊天）
├── config.py            # 应用配置（基于 pydantic-settings）
├── schemas.py           # 请求/响应数据模型
├── requirements.txt     # 项目依赖
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略配置
└── README.md            # 项目说明
```

## 切换模型

在 `chat.py` 中替换 `get_llm()` 实现即可切换到其他模型，例如：

- **OpenAI**：`from langchain_openai import ChatOpenAI`
- **Anthropic Claude**：`from langchain_anthropic import ChatAnthropic`
- **通义千问**：`from langchain_community.chat_models.tongyi import ChatTongyi`
- **本地 Ollama**：`from langchain_community.chat_models import ChatOllama`

## 常见问题

**Q: 启动时报 `DEEPSEEK_API_KEY 未配置`？**
A: 请确认 `.env` 文件已创建在 `backend/` 目录下，且 `DEEPSEEK_API_KEY` 已设置为有效值。

**Q: 流式接口没有逐字返回？**
A: 请检查网络是否能访问 `https://api.deepseek.com`，以及 API Key 是否有效。

**Q: 想要使用其他模型？**
A: 修改 `chat.py` 中的 `get_llm()`，并在 `requirements.txt` 中添加对应依赖。