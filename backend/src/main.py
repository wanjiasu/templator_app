"""
FastAPI 应用入口文件
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="FastAPI Backend",
        description="A simple FastAPI backend for testing",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # 添加 CORS 中间件
    cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
    # 简单解析 CORS_ORIGINS 字符串为列表
    if cors_origins.startswith('[') and cors_origins.endswith(']'):
        cors_origins = [origin.strip(' "') for origin in cors_origins[1:-1].split(',')]
    else:
        cors_origins = [cors_origins]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 基本路由
    @app.get("/")
    async def root():
        return {"message": "Welcome to FastAPI Backend!"}
    
    # 测试路由
    @app.get("/test")
    async def test():
        return {"message": "Hello World!", "status": "success"}
    
    # 健康检查路由
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "Service is running"}
    
    return app


# 创建应用实例
app = create_app()


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("Starting FastAPI Backend...")


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("Shutting down FastAPI Backend...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )