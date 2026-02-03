"""笔记 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter()


@router.post("", response_model=NoteResponse)
async def create_or_update_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建或更新笔记（一个题目只有一个笔记）"""
    # 查找现有笔记
    result = await db.execute(
        select(Note).where(Note.problem_id == note_data.problem_id)
    )
    note = result.scalar_one_or_none()
    
    if note:
        # 更新现有笔记
        note.approach = note_data.approach
        note.code = note_data.code
        note.language = note_data.language
        note.time_complexity = note_data.time_complexity
        note.space_complexity = note_data.space_complexity
        note.key_points = note_data.key_points
    else:
        # 创建新笔记
        note = Note(
            problem_id=note_data.problem_id,
            approach=note_data.approach,
            code=note_data.code,
            language=note_data.language,
            time_complexity=note_data.time_complexity,
            space_complexity=note_data.space_complexity,
            key_points=note_data.key_points,
        )
        db.add(note)
    
    await db.commit()
    await db.refresh(note)
    
    return note


@router.get("/{problem_id}", response_model=NoteResponse | None)
async def get_note(problem_id: int, db: AsyncSession = Depends(get_db)):
    """获取题目笔记"""
    result = await db.execute(
        select(Note).where(Note.problem_id == problem_id)
    )
    note = result.scalar_one_or_none()
    
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    """删除笔记"""
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    
    await db.delete(note)
    await db.commit()
    
    return {"message": "删除成功"}
