"""进度数据模式"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProgressBase(BaseModel):
    """进度基础模式"""
    # 新状态模型: not_started / in_progress / mastered
    status: str = Field(default="not_started", description="状态: not_started/in_progress/mastered")
    mastery_level: int = Field(default=0, ge=0, le=5, description="掌握程度(已完成复习轮次) 0-5")


class ProgressUpdate(ProgressBase):
    """更新进度（保留用于高级手动调整）"""
    pass


class ProgressResponse(ProgressBase):
    """进度响应"""
    id: int
    problem_id: int
    attempt_count: int
    first_solved: Optional[datetime] = None
    last_attempt: Optional[datetime] = None
    # 新增: 复习进度信息
    completed_reviews: int = Field(default=0, description="已完成复习轮次")
    total_reviews: int = Field(default=5, description="总复习轮次")
    
    class Config:
        from_attributes = True
