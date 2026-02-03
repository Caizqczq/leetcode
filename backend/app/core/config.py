"""应用配置"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用信息
    APP_NAME: str = "LeetCode Hot 100 管理工具"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./leetcode.db"
    
    # CORS 配置
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # 艾宾浩斯复习间隔（天数）
    REVIEW_INTERVALS: list[int] = [1, 2, 4, 7, 15]
    
    class Config:
        env_file = ".env"


settings = Settings()
