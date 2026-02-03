"""复习 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import ReviewPlan, Progress, Problem
from app.schemas.review import ReviewPlanResponse, TodayReviewResponse, ProblemInReview
from app.services.review_service import get_today_reviews, complete_review

router = APIRouter()


@router.get("/today", response_model=TodayReviewResponse)
async def get_today_review_list(db: AsyncSession = Depends(get_db)):
    """获取今日待复习、逾期和即将复习的题目"""
    reviews = await get_today_reviews(db)
    
    async def build_response(plans: list[ReviewPlan]) -> list[ReviewPlanResponse]:
        """构建复习计划响应"""
        result = []
        for plan in plans:
            # 获取关联的进度和题目信息
            progress_result = await db.execute(
                select(Progress)
                .options(selectinload(Progress.problem))
                .where(Progress.id == plan.progress_id)
            )
            progress = progress_result.scalar_one_or_none()
            
            problem_data = None
            if progress and progress.problem:
                problem_data = ProblemInReview(
                    id=progress.problem.id,
                    leetcode_id=progress.problem.leetcode_id,
                    title=progress.problem.title,
                    title_cn=progress.problem.title_cn,
                    difficulty=progress.problem.difficulty,
                    category=progress.problem.category,
                )
            
            result.append(ReviewPlanResponse(
                id=plan.id,
                progress_id=plan.progress_id,
                scheduled_date=plan.scheduled_date,
                review_round=plan.review_round,
                completed=plan.completed,
                completed_at=plan.completed_at,
                problem=problem_data,
            ))
        
        return result
    
    return TodayReviewResponse(
        today=await build_response(reviews["today"]),
        overdue=await build_response(reviews["overdue"]),
        upcoming=await build_response(reviews["upcoming"]),
    )


@router.put("/{review_id}/complete", response_model=ReviewPlanResponse)
async def mark_review_complete(review_id: int, db: AsyncSession = Depends(get_db)):
    """标记复习完成"""
    review_plan = await complete_review(db, review_id)
    
    if not review_plan:
        raise HTTPException(status_code=404, detail="复习计划不存在")
    
    # 获取关联的题目信息
    progress_result = await db.execute(
        select(Progress)
        .options(selectinload(Progress.problem))
        .where(Progress.id == review_plan.progress_id)
    )
    progress = progress_result.scalar_one_or_none()
    
    problem_data = None
    if progress and progress.problem:
        problem_data = ProblemInReview(
            id=progress.problem.id,
            leetcode_id=progress.problem.leetcode_id,
            title=progress.problem.title,
            title_cn=progress.problem.title_cn,
            difficulty=progress.problem.difficulty,
            category=progress.problem.category,
        )
    
    return ReviewPlanResponse(
        id=review_plan.id,
        progress_id=review_plan.progress_id,
        scheduled_date=review_plan.scheduled_date,
        review_round=review_plan.review_round,
        completed=review_plan.completed,
        completed_at=review_plan.completed_at,
        problem=problem_data,
    )


@router.get("", response_model=list[ReviewPlanResponse])
async def get_all_reviews(
    completed: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    """获取所有复习计划"""
    query = select(ReviewPlan).order_by(ReviewPlan.scheduled_date)
    
    if completed is not None:
        query = query.where(ReviewPlan.completed == completed)
    
    result = await db.execute(query)
    plans = result.scalars().all()
    
    response = []
    for plan in plans:
        # 获取关联的题目信息
        progress_result = await db.execute(
            select(Progress)
            .options(selectinload(Progress.problem))
            .where(Progress.id == plan.progress_id)
        )
        progress = progress_result.scalar_one_or_none()
        
        problem_data = None
        if progress and progress.problem:
            problem_data = ProblemInReview(
                id=progress.problem.id,
                leetcode_id=progress.problem.leetcode_id,
                title=progress.problem.title,
                title_cn=progress.problem.title_cn,
                difficulty=progress.problem.difficulty,
                category=progress.problem.category,
            )
        
        response.append(ReviewPlanResponse(
            id=plan.id,
            progress_id=plan.progress_id,
            scheduled_date=plan.scheduled_date,
            review_round=plan.review_round,
            completed=plan.completed,
            completed_at=plan.completed_at,
            problem=problem_data,
        ))
    
    return response
