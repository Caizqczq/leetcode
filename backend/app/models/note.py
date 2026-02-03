"""笔记模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Note(Base):
    """题解笔记"""
    
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    
    # 笔记内容
    approach = Column(Text, comment="解题思路")
    code = Column(Text, comment="代码")
    language = Column(String(20), default="python", comment="代码语言")
    time_complexity = Column(String(50), comment="时间复杂度")
    space_complexity = Column(String(50), comment="空间复杂度")
    key_points = Column(Text, comment="关键点/易错点")
    
    # 时间记录
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    problem = relationship("Problem", back_populates="notes")
    
    def __repr__(self):
        return f"<Note problem_id={self.problem_id}>"
