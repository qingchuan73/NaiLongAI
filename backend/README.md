# NaiLongAI Backend

基于 FastAPI + LangChain + 硅基流动（SiliconFlow）构建的 AI 对话后端服务。

## 功能特性

- 🚀 **FastAPI**：高性能异步 Web 框架
- 🔗 **LangChain**：LLM 应用编排框架
- 🌊 **硅基流动 SiliconFlow**：兼容 OpenAI 协议的高性价比模型平台
- 🤖 **DeepSeek-V3**（默认）：通过硅基流动调用，能力强、成本低
- 💬 **多轮对话**：支持 `messages` 数组传递历史消息
- ⚙️ **配置管理**：通过 `.env` 文件和环境变量管理

## 环境要求

- Python 3.10+
- pip
- 硅基流动 API Key（[申请地址](https://cloud.siliconflow.cn)）

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
# 编辑 .env，至少填入 SILICONFLOW_API_KEY
```

`.env` 示例：

```env
SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxxxxx
SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V3
SILICONFLOW_TEMPERATURE=0.7
```

### 4. 启动服务

```bash
# 方式一：使用 uvicorn（推荐）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式二：直接运行
python main.py
```

### 5. （可选）单独测试对话模块

```bash
python chat.py
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

### 3. `POST /chat` — 聊天接口

**单轮对话请求体：**

```json
{
  "message": "你好，请介绍下你自己"
}
```

**多轮对话请求体：**

```json
{
  "messages": [
    {"role": "system", "content": "你是一位诗人"},
    {"role": "user", "content": "写一首关于秋天的诗"}
  ]
}
```

**响应：**

```json
{
  "content": "AI 的回复内容..."
}
```

**使用 curl 测试：**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

**使用 PowerShell 测试：**

```powershell
$body = @{message = "你好"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" `
  -Method POST -ContentType "application/json" -Body $body
```

## 项目结构

```
backend/
├── main.py              # FastAPI 应用入口（路由定义）
├── chat.py              # LangChain + 硅基流动 对话模块
├── config.py            # 应用配置（基于 pydantic-settings）
├── schemas.py           # 请求/响应数据模型
├── requirements.txt     # 项目依赖
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略配置
└── README.md            # 项目说明
```

## 切换模型

在 `.env` 中修改 `SILICONFLOW_MODEL` 即可切换模型，硅基流动支持的常用模型：

| 模型 ID | 说明 |
| --- | --- |
| `deepseek-ai/DeepSeek-V3` | 默认，强综合能力 |
| `deepseek-ai/DeepSeek-R1` | 强推理 |
| `Qwen/Qwen3-235B-A22B-Instruct-2507` | 通义千问 3 旗舰 |
| `Pro/Qwen/Qwen2.5-7B-Instruct` | 通义千问 7B，轻量 |

完整模型列表：https://docs.siliconflow.cn/cn/api-reference/models

## 关于硅基流动

硅基流动（SiliconFlow）提供 **OpenAI 兼容** 的 Chat Completions 接口，因此我们直接复用 LangChain 官方的 `langchain-openai` 包，通过设置 `base_url=https://api.siliconflow.cn/v1` 来调用，无需额外的 provider 包。

## 常见问题

**Q: 启动时报 `SILICONFLOW_API_KEY 未配置`？**
A: 请确认 `.env` 文件已创建在 `backend/` 目录下，且 `SILICONFLOW_API_KEY` 已设置为有效值。

**Q: 模型返回为空或乱码？**
A: 请检查网络是否能访问 `https://api.siliconflow.cn`，以及模型 ID 是否拼写正确。