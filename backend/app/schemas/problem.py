"""题目数据模式"""
from typing import Optional
from pydantic import BaseModel


class ProblemBase(BaseModel):
    """题目基础模式"""
    leetcode_id: int
    title: str
    title_cn: str
    difficulty: str
    category: str
    url: Optional[str] = None


class ProblemCreate(ProblemBase):
    """创建题目"""
    pass


class ProgressInProblem(BaseModel):
    """题目中的进度信息"""
    status: str = "not_started"
    attempt_count: int = 0
    mastery_level: int = 0
    # 复习进度信息
    completed_reviews: int = 0
    total_reviews: int = 5
    
    class Config:
        from_attributes = True


class TagInProblem(BaseModel):
    """题目中的标签信息"""
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True


class ProblemResponse(ProblemBase):
    """题目响应"""
    id: int
    progress: Optional[ProgressInProblem] = None
    tags: list[TagInProblem] = []
    
    class Config:
        from_attributes = True


class ProblemListResponse(BaseModel):
    """题目列表响应"""
    total: int
    items: list[ProblemResponse]
