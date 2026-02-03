"""进度数据模式"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProgressBase(BaseModel):
    """进度基础模式"""
    status: str = Field(default="not_started", description="状态: not_started/attempted/reviewing/mastered")
    mastery_level: int = Field(default=0, ge=0, le=5, description="掌握程度 0-5")


class ProgressUpdate(ProgressBase):
    """更新进度"""
    pass


class ProgressResponse(ProgressBase):
    """进度响应"""
    id: int
    problem_id: int
    attempt_count: int
    first_solved: Optional[datetime] = None
    last_attempt: Optional[datetime] = None
    
    class Config:
        from_attributes = True
