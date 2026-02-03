"""初始化数据服务"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Problem, Progress, Tag
from app.data.hot100 import HOT_100_PROBLEMS, DEFAULT_TAGS, get_leetcode_url


async def init_problems(db: AsyncSession) -> None:
    """初始化 Hot 100 题目数据"""
    # 检查是否已有数据
    result = await db.execute(select(Problem).limit(1))
    if result.scalar_one_or_none():
        return  # 已有数据，跳过
    
    # 插入题目数据
    for problem_data in HOT_100_PROBLEMS:
        url = get_leetcode_url(problem_data["leetcode_id"], problem_data["title"])
        problem = Problem(
            leetcode_id=problem_data["leetcode_id"],
            title=problem_data["title"],
            title_cn=problem_data["title_cn"],
            difficulty=problem_data["difficulty"],
            category=problem_data["category"],
            url=url,
        )
        db.add(problem)
    
    await db.commit()
    
    # 为每个题目创建初始进度记录
    result = await db.execute(select(Problem))
    problems = result.scalars().all()
    
    for problem in problems:
        progress = Progress(problem_id=problem.id)
        db.add(progress)
    
    await db.commit()


async def init_tags(db: AsyncSession) -> None:
    """初始化默认标签"""
    # 检查是否已有标签
    result = await db.execute(select(Tag).limit(1))
    if result.scalar_one_or_none():
        return  # 已有数据，跳过
    
    # 插入默认标签
    for tag_data in DEFAULT_TAGS:
        tag = Tag(name=tag_data["name"], color=tag_data["color"])
        db.add(tag)
    
    await db.commit()


async def init_all_data(db: AsyncSession) -> None:
    """初始化所有数据"""
    await init_problems(db)
    await init_tags(db)
