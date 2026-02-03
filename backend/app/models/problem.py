"""题目模型"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Problem(Base):
    """LeetCode 题目"""
    
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    leetcode_id = Column(Integer, unique=True, index=True, comment="LeetCode 题目编号")
    title = Column(String(200), nullable=False, comment="英文标题")
    title_cn = Column(String(200), nullable=False, comment="中文标题")
    difficulty = Column(String(20), nullable=False, comment="难度: Easy/Medium/Hard")
    category = Column(String(50), nullable=False, comment="题目分类")
    url = Column(String(500), comment="LeetCode 链接")
    
    # 关联关系
    progress = relationship("Progress", back_populates="problem", uselist=False)
    notes = relationship("Note", back_populates="problem")
    problem_tags = relationship("ProblemTag", back_populates="problem")
    
    def __repr__(self):
        return f"<Problem {self.leetcode_id}: {self.title_cn}>"
