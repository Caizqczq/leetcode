"""标签模型"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Tag(Base):
    """标签"""
    
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="标签名称")
    color = Column(String(20), default="#409EFF", comment="标签颜色")
    
    # 关联关系
    problem_tags = relationship("ProblemTag", back_populates="tag")
    
    def __repr__(self):
        return f"<Tag {self.name}>"


class ProblemTag(Base):
    """题目-标签关联表"""
    
    __tablename__ = "problem_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    
    # 关联关系
    problem = relationship("Problem", back_populates="problem_tags")
    tag = relationship("Tag", back_populates="problem_tags")
