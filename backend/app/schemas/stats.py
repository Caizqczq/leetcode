"""统计数据模式"""
from pydantic import BaseModel


class DifficultyStats(BaseModel):
    """难度统计"""
    easy: int = 0
    medium: int = 0
    hard: int = 0


class StatusStats(BaseModel):
    """状态统计"""
    not_started: int = 0
    attempted: int = 0
    reviewing: int = 0
    mastered: int = 0


class CategoryStats(BaseModel):
    """分类统计"""
    category: str
    total: int
    completed: int


class DailyStats(BaseModel):
    """每日统计"""
    date: str
    count: int


class StatsResponse(BaseModel):
    """统计响应"""
    total_problems: int
    completed_count: int
    completion_rate: float
    difficulty_stats: DifficultyStats
    status_stats: StatusStats
    category_stats: list[CategoryStats]
    daily_stats: list[DailyStats]
