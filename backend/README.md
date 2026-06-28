# NaiLongAI Backend

基于 FastAPI 构建的后端服务。

## 环境要求

- Python 3.10+
- pip

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
# 根据需要修改 .env 中的配置
```

### 4. 启动服务

```bash
python main.py
```

或者使用 uvicorn 直接启动：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后访问：

- API 根路径: http://localhost:8000
- 交互式 API 文档（Swagger UI）: http://localhost:8000/docs
- 替代 API 文档（ReDoc）: http://localhost:8000/redoc

## 项目结构

```
backend/
├── main.py              # FastAPI 应用入口
├── requirements.txt     # 项目依赖
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略文件
└── README.md            # 项目说明
```

## 接口说明

| 方法 | 路径       | 说明           |
| ---- | ---------- | -------------- |
| GET  | `/`        | 欢迎接口       |
| GET  | `/config`  | 获取应用配置   |