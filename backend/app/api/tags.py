"""标签 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Tag, ProblemTag
from app.schemas.tag import TagCreate, TagResponse

router = APIRouter()


@router.get("", response_model=list[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    """获取所有标签"""
    result = await db.execute(select(Tag).order_by(Tag.name))
    tags = result.scalars().all()
    return tags


@router.post("", response_model=TagResponse)
async def create_tag(tag_data: TagCreate, db: AsyncSession = Depends(get_db)):
    """创建标签"""
    # 检查是否已存在
    result = await db.execute(select(Tag).where(Tag.name == tag_data.name))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="标签已存在")
    
    tag = Tag(name=tag_data.name, color=tag_data.color)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    
    return tag


@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """删除标签"""
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    await db.delete(tag)
    await db.commit()
    
    return {"message": "删除成功"}


@router.post("/{problem_id}/tags/{tag_id}")
async def add_tag_to_problem(
    problem_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_db),
):
    """为题目添加标签"""
    # 检查是否已存在关联
    result = await db.execute(
        select(ProblemTag).where(
            (ProblemTag.problem_id == problem_id) & (ProblemTag.tag_id == tag_id)
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return {"message": "标签已添加"}
    
    problem_tag = ProblemTag(problem_id=problem_id, tag_id=tag_id)
    db.add(problem_tag)
    await db.commit()
    
    return {"message": "添加成功"}


@router.delete("/{problem_id}/tags/{tag_id}")
async def remove_tag_from_problem(
    problem_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_db),
):
    """从题目移除标签"""
    result = await db.execute(
        select(ProblemTag).where(
            (ProblemTag.problem_id == problem_id) & (ProblemTag.tag_id == tag_id)
        )
    )
    problem_tag = result.scalar_one_or_none()
    
    if problem_tag:
        await db.delete(problem_tag)
        await db.commit()
    
    return {"message": "移除成功"}
