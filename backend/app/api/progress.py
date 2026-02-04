"""进度 API"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models import Progress, ReviewPlan
from app.schemas.progress import ProgressUpdate, ProgressResponse
from app.services.review_service import generate_review_plans

router = APIRouter()


async def get_review_stats(db: AsyncSession, progress_id: int) -> tuple[int, int]:
    """获取复习统计：(已完成轮次, 总轮次)"""
    # 查询已完成的复习轮次数
    completed_result = await db.execute(
        select(func.count()).where(
            ReviewPlan.progress_id == progress_id,
            ReviewPlan.completed == True
        )
    )
    completed = completed_result.scalar() or 0
    
    # 查询总复习轮次数
    total_result = await db.execute(
        select(func.count()).where(ReviewPlan.progress_id == progress_id)
    )
    total = total_result.scalar() or 0
    
    return completed, total if total > 0 else 5


def build_progress_response(progress: Progress, completed_reviews: int, total_reviews: int, is_first_complete: bool = False) -> dict:
    """构建进度响应，包含复习进度信息"""
    return {
        "id": progress.id,
        "problem_id": progress.problem_id,
        "status": progress.status,
        "mastery_level": progress.mastery_level,
        "attempt_count": progress.attempt_count,
        "first_solved": progress.first_solved,
        "last_attempt": progress.last_attempt,
        "completed_reviews": completed_reviews,
        "total_reviews": total_reviews,
        "is_first_complete": is_first_complete,
    }


@router.post("/{problem_id}/complete", response_model=ProgressResponse)
async def mark_complete(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    一键标记完成
    - 自动将状态从 not_started 变为 in_progress
    - 自动生成复习计划
    - 增加尝试次数
    """
    # 查找进度记录
    result = await db.execute(
        select(Progress).where(Progress.problem_id == problem_id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="进度记录不存在")
    
    # 记录是否首次完成
    is_first_time = progress.status == "not_started"
    
    # 自动设置状态为进行中（如果还未开始）
    if progress.status == "not_started":
        progress.status = "in_progress"
        progress.first_solved = datetime.utcnow()
    
    # 更新尝试次数和时间
    progress.attempt_count += 1
    progress.last_attempt = datetime.utcnow()
    
    await db.commit()
    await db.refresh(progress)
    
    # 首次完成时生成复习计划
    if is_first_time:
        await generate_review_plans(db, progress.id)
    
    # 获取复习统计
    completed_reviews, total_reviews = await get_review_stats(db, progress.id)
    
    return build_progress_response(progress, completed_reviews, total_reviews, is_first_complete=is_first_time)


@router.put("/{problem_id}", response_model=ProgressResponse)
async def update_progress(
    problem_id: int,
    progress_update: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    手动更新题目进度（高级选项）
    保留此接口用于特殊情况下的手动调整
    """
    # 查找进度记录
    result = await db.execute(
        select(Progress).where(Progress.problem_id == problem_id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="进度记录不存在")
    
    # 记录旧状态
    old_status = progress.status
    
    # 更新状态
    progress.status = progress_update.status
    progress.mastery_level = progress_update.mastery_level
    progress.attempt_count += 1
    progress.last_attempt = datetime.utcnow()
    
    # 如果首次完成
    if old_status == "not_started" and progress_update.status in ["in_progress", "mastered"]:
        progress.first_solved = datetime.utcnow()
    
    await db.commit()
    await db.refresh(progress)
    
    # 如果状态变为进行中，生成复习计划
    if progress_update.status == "in_progress" and old_status == "not_started":
        await generate_review_plans(db, progress.id)
    
    # 获取复习统计
    completed_reviews, total_reviews = await get_review_stats(db, progress.id)
    
    return build_progress_response(progress, completed_reviews, total_reviews)


@router.get("/{problem_id}", response_model=ProgressResponse)
async def get_progress(problem_id: int, db: AsyncSession = Depends(get_db)):
    """获取题目进度"""
    result = await db.execute(
        select(Progress).where(Progress.problem_id == problem_id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="进度记录不存在")
    
    # 获取复习统计
    completed_reviews, total_reviews = await get_review_stats(db, progress.id)
    
    return build_progress_response(progress, completed_reviews, total_reviews)
