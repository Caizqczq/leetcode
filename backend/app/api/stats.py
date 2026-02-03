"""统计 API"""
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models import Problem, Progress
from app.schemas.stats import StatsResponse, DifficultyStats, StatusStats, CategoryStats, DailyStats

router = APIRouter()


@router.get("", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """获取统计数据"""
    # 总题目数
    total_result = await db.execute(select(func.count(Problem.id)))
    total_problems = total_result.scalar()
    
    # 已完成数量（状态不是 not_started 的）
    completed_result = await db.execute(
        select(func.count(Progress.id)).where(Progress.status != "not_started")
    )
    completed_count = completed_result.scalar()
    
    # 完成率
    completion_rate = round(completed_count / total_problems * 100, 1) if total_problems > 0 else 0
    
    # 难度统计
    difficulty_stats = DifficultyStats()
    for difficulty in ["Easy", "Medium", "Hard"]:
        result = await db.execute(
            select(func.count(Problem.id)).where(Problem.difficulty == difficulty)
        )
        count = result.scalar()
        if difficulty == "Easy":
            difficulty_stats.easy = count
        elif difficulty == "Medium":
            difficulty_stats.medium = count
        else:
            difficulty_stats.hard = count
    
    # 状态统计
    status_stats = StatusStats()
    for status in ["not_started", "attempted", "reviewing", "mastered"]:
        result = await db.execute(
            select(func.count(Progress.id)).where(Progress.status == status)
        )
        count = result.scalar()
        setattr(status_stats, status, count)
    
    # 分类统计
    category_result = await db.execute(
        select(Problem.category, func.count(Problem.id))
        .group_by(Problem.category)
        .order_by(Problem.category)
    )
    category_data = category_result.fetchall()
    
    category_stats = []
    for category, total in category_data:
        # 计算该分类已完成数量
        completed_in_category = await db.execute(
            select(func.count(Progress.id))
            .select_from(Progress)
            .join(Problem)
            .where(Problem.category == category)
            .where(Progress.status != "not_started")
        )
        completed = completed_in_category.scalar()
        category_stats.append(CategoryStats(
            category=category,
            total=total,
            completed=completed,
        ))
    
    # 每日统计（最近30天）
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_result = await db.execute(
        select(Progress.last_attempt)
        .where(Progress.last_attempt >= thirty_days_ago)
        .where(Progress.last_attempt.isnot(None))
    )
    daily_data = daily_result.fetchall()
    
    # 按日期统计
    date_counts = defaultdict(int)
    for row in daily_data:
        if row[0]:
            date_str = row[0].strftime("%Y-%m-%d")
            date_counts[date_str] += 1
    
    daily_stats = [
        DailyStats(date=date, count=count)
        for date, count in sorted(date_counts.items())
    ]
    
    return StatsResponse(
        total_problems=total_problems,
        completed_count=completed_count,
        completion_rate=completion_rate,
        difficulty_stats=difficulty_stats,
        status_stats=status_stats,
        category_stats=category_stats,
        daily_stats=daily_stats,
    )
