"""标签数据模式"""
from pydantic import BaseModel


class TagBase(BaseModel):
    """标签基础模式"""
    name: str
    color: str = "#409EFF"


class TagCreate(TagBase):
    """创建标签"""
    pass


class TagResponse(TagBase):
    """标签响应"""
    id: int
    
    class Config:
        from_attributes = True
