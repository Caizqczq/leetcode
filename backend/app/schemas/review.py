"""复习计划数据模式"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewPlanBase(BaseModel):
    """复习计划基础模式"""
    scheduled_date: datetime
    review_round: int


class ProblemInReview(BaseModel):
    """复习中的题目信息"""
    id: int
    leetcode_id: int
    title: str
    title_cn: str
    difficulty: str
    category: str
    
    class Config:
        from_attributes = True


class ReviewPlanResponse(ReviewPlanBase):
    """复习计划响应"""
    id: int
    progress_id: int
    completed: bool
    completed_at: Optional[datetime] = None
    problem: Optional[ProblemInReview] = None
    
    class Config:
        from_attributes = True


class TodayReviewResponse(BaseModel):
    """今日待复习响应"""
    today: list[ReviewPlanResponse]
    overdue: list[ReviewPlanResponse]
    upcoming: list[ReviewPlanResponse]
