"""进度 API"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Progress
from app.schemas.progress import ProgressUpdate, ProgressResponse
from app.services.review_service import generate_review_plans

router = APIRouter()


@router.put("/{problem_id}", response_model=ProgressResponse)
async def update_progress(
    problem_id: int,
    progress_update: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新题目进度"""
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
    if old_status == "not_started" and progress_update.status in ["attempted", "reviewing", "mastered"]:
        progress.first_solved = datetime.utcnow()
    
    await db.commit()
    await db.refresh(progress)
    
    # 如果状态变为已做或复习中，生成复习计划
    if progress_update.status in ["attempted", "reviewing"] and old_status == "not_started":
        await generate_review_plans(db, progress.id)
    
    return progress


@router.get("/{problem_id}", response_model=ProgressResponse)
async def get_progress(problem_id: int, db: AsyncSession = Depends(get_db)):
    """获取题目进度"""
    result = await db.execute(
        select(Progress).where(Progress.problem_id == problem_id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="进度记录不存在")
    
    return progress
