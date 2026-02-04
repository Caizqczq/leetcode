"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import init_db
from app.api import problems, progress, notes, tags, reviews, stats

# 前端静态文件目录
STATIC_DIR = Path(__file__).parent.parent.parent / "static"


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


@app.get("/api")
async def api_root():
    """API 健康检查"""
    return {"message": "LeetCode Hot 100 管理工具 API", "version": settings.APP_VERSION}


# 托管前端静态文件（生产环境）
if STATIC_DIR.exists():
    # 挂载静态资源（js, css, images 等）
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")
    
    # 所有非 API 路由返回 index.html（支持 Vue Router 的 history 模式）
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """服务单页应用"""
        # 如果请求的是静态文件且存在，返回该文件
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # 否则返回 index.html（让前端路由处理）
        return FileResponse(STATIC_DIR / "index.html")
