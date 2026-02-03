"""题目 API"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Problem, Progress, ProblemTag, Tag
from app.schemas.problem import ProblemResponse, ProblemListResponse, TagInProblem, ProgressInProblem
from app.services.init_data import init_all_data

router = APIRouter()


@router.get("", response_model=ProblemListResponse)
async def get_problems(
    difficulty: Optional[str] = Query(None, description="难度筛选: Easy/Medium/Hard"),
    category: Optional[str] = Query(None, description="分类筛选"),
    status: Optional[str] = Query(None, description="状态筛选: not_started/attempted/reviewing/mastered"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    tag_id: Optional[int] = Query(None, description="标签ID筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取题目列表（支持筛选和分页）"""
    # 确保数据已初始化
    await init_all_data(db)
    
    # 构建查询
    query = select(Problem).options(
        selectinload(Problem.progress),
        selectinload(Problem.problem_tags).selectinload(ProblemTag.tag)
    )
    
    # 难度筛选
    if difficulty:
        query = query.where(Problem.difficulty == difficulty)
    
    # 分类筛选
    if category:
        query = query.where(Problem.category == category)
    
    # 搜索
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Problem.title.ilike(search_pattern)) | 
            (Problem.title_cn.ilike(search_pattern)) |
            (Problem.leetcode_id == int(search) if search.isdigit() else False)
        )
    
    # 标签筛选
    if tag_id:
        query = query.join(ProblemTag).where(ProblemTag.tag_id == tag_id)
    
    # 状态筛选
    if status:
        query = query.join(Progress).where(Progress.status == status)
    
    # 排序（按 id 保持官方顺序）
    query = query.order_by(Problem.id)
    
    # 计算总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    # 执行查询
    result = await db.execute(query)
    problems = result.scalars().unique().all()
    
    # 构建响应
    items = []
    for problem in problems:
        # 处理进度信息
        progress_data = None
        if problem.progress:
            progress_data = ProgressInProblem(
                status=problem.progress.status,
                attempt_count=problem.progress.attempt_count,
                mastery_level=problem.progress.mastery_level,
            )
        
        # 处理标签信息
        tags_data = [
            TagInProblem(id=pt.tag.id, name=pt.tag.name, color=pt.tag.color)
            for pt in problem.problem_tags
        ]
        
        items.append(ProblemResponse(
            id=problem.id,
            leetcode_id=problem.leetcode_id,
            title=problem.title,
            title_cn=problem.title_cn,
            difficulty=problem.difficulty,
            category=problem.category,
            url=problem.url,
            progress=progress_data,
            tags=tags_data,
        ))
    
    return ProblemListResponse(total=total, items=items)


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取所有分类"""
    result = await db.execute(
        select(Problem.category).distinct().order_by(Problem.category)
    )
    categories = [row[0] for row in result.fetchall()]
    return {"categories": categories}


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    """获取题目详情"""
    result = await db.execute(
        select(Problem)
        .options(
            selectinload(Problem.progress),
            selectinload(Problem.problem_tags).selectinload(ProblemTag.tag)
        )
        .where(Problem.id == problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="题目不存在")
    
    # 处理进度信息
    progress_data = None
    if problem.progress:
        progress_data = ProgressInProblem(
            status=problem.progress.status,
            attempt_count=problem.progress.attempt_count,
            mastery_level=problem.progress.mastery_level,
        )
    
    # 处理标签信息
    tags_data = [
        TagInProblem(id=pt.tag.id, name=pt.tag.name, color=pt.tag.color)
        for pt in problem.problem_tags
    ]
    
    return ProblemResponse(
        id=problem.id,
        leetcode_id=problem.leetcode_id,
        title=problem.title,
        title_cn=problem.title_cn,
        difficulty=problem.difficulty,
        category=problem.category,
        url=problem.url,
        progress=progress_data,
        tags=tags_data,
    )
