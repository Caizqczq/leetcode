"""复习计划服务"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models import ReviewPlan, Progress
from app.core.config import settings


async def generate_review_plans(db: AsyncSession, progress_id: int) -> None:
    """
    为已完成的题目生成艾宾浩斯复习计划
    复习间隔: 1天、2天、4天、7天、15天
    """
    # 删除该进度的所有未完成复习计划
    existing_plans = await db.execute(
        select(ReviewPlan).where(
            and_(
                ReviewPlan.progress_id == progress_id,
                ReviewPlan.completed == False
            )
        )
    )
    for plan in existing_plans.scalars().all():
        await db.delete(plan)
    
    # 生成新的复习计划
    now = datetime.utcnow()
    for round_num, interval in enumerate(settings.REVIEW_INTERVALS, start=1):
        scheduled_date = now + timedelta(days=interval)
        review_plan = ReviewPlan(
            progress_id=progress_id,
            scheduled_date=scheduled_date,
            review_round=round_num,
            completed=False,
        )
        db.add(review_plan)
    
    await db.commit()


async def get_today_reviews(db: AsyncSession) -> dict:
    """获取今日待复习、逾期和即将复习的题目"""
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    # 今日待复习
    today_result = await db.execute(
        select(ReviewPlan).where(
            and_(
                ReviewPlan.scheduled_date >= today_start,
                ReviewPlan.scheduled_date <= today_end,
                ReviewPlan.completed == False
            )
        ).order_by(ReviewPlan.scheduled_date)
    )
    today_plans = today_result.scalars().all()
    
    # 逾期未复习
    overdue_result = await db.execute(
        select(ReviewPlan).where(
            and_(
                ReviewPlan.scheduled_date < today_start,
                ReviewPlan.completed == False
            )
        ).order_by(ReviewPlan.scheduled_date)
    )
    overdue_plans = overdue_result.scalars().all()
    
    # 未来7天待复习
    upcoming_end = today_start + timedelta(days=7)
    upcoming_result = await db.execute(
        select(ReviewPlan).where(
            and_(
                ReviewPlan.scheduled_date > today_end,
                ReviewPlan.scheduled_date <= upcoming_end,
                ReviewPlan.completed == False
            )
        ).order_by(ReviewPlan.scheduled_date)
    )
    upcoming_plans = upcoming_result.scalars().all()
    
    return {
        "today": today_plans,
        "overdue": overdue_plans,
        "upcoming": upcoming_plans,
    }


async def count_completed_reviews(db: AsyncSession, progress_id: int) -> int:
    """统计已完成的复习轮次数"""
    result = await db.execute(
        select(func.count()).where(
            and_(
                ReviewPlan.progress_id == progress_id,
                ReviewPlan.completed == True
            )
        )
    )
    return result.scalar() or 0


async def complete_review(db: AsyncSession, review_id: int) -> ReviewPlan | None:
    """
    标记复习完成
    - 自动更新掌握程度（= 已完成复习轮次）
    - 5轮全部完成时自动标记为已掌握
    """
    result = await db.execute(select(ReviewPlan).where(ReviewPlan.id == review_id))
    review_plan = result.scalar_one_or_none()
    
    if not review_plan:
        return None
    
    # 标记复习完成
    review_plan.completed = True
    review_plan.completed_at = datetime.utcnow()
    
    # 获取关联的进度记录
    progress_result = await db.execute(
        select(Progress).where(Progress.id == review_plan.progress_id)
    )
    progress = progress_result.scalar_one_or_none()
    
    if progress:
        # 计算已完成的复习轮次（包括刚刚完成的这一轮）
        completed_count = await count_completed_reviews(db, progress.id)
        # 因为当前这轮还没提交，需要+1
        completed_count += 1
        
        # 自动更新掌握程度
        progress.mastery_level = min(completed_count, 5)
        progress.last_attempt = datetime.utcnow()
        
        # 5轮全部完成 → 自动标记为已掌握
        if completed_count >= 5:
            progress.status = "mastered"
    
    await db.commit()
    await db.refresh(review_plan)
    
    return review_plan
