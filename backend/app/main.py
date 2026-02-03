"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api import problems, progress, notes, tags, reviews, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(problems.router, prefix="/api/problems", tags=["题目"])
app.include_router(progress.router, prefix="/api/progress", tags=["进度"])
app.include_router(notes.router, prefix="/api/notes", tags=["笔记"])
app.include_router(tags.router, prefix="/api/tags", tags=["标签"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["复习"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计"])


@app.get("/")
async def root():
    """健康检查"""
    return {"message": "LeetCode Hot 100 管理工具 API", "version": settings.APP_VERSION}
