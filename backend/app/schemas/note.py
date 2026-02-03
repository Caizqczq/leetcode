"""笔记数据模式"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NoteBase(BaseModel):
    """笔记基础模式"""
    approach: Optional[str] = None
    code: Optional[str] = None
    language: str = "python"
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    key_points: Optional[str] = None


class NoteCreate(NoteBase):
    """创建笔记"""
    problem_id: int


class NoteUpdate(NoteBase):
    """更新笔记"""
    pass


class NoteResponse(NoteBase):
    """笔记响应"""
    id: int
    problem_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
