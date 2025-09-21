"""
FastAPI 应用入口文件
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings


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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
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