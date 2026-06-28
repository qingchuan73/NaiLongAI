from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="NaiLongAI Backend",
    description="NaiLongAI 后端服务",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Hello, NaiLongAI!"}


@app.get("/config")
async def get_config():
    return {
        "app_name": os.getenv("APP_NAME", "NaiLongAI"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)