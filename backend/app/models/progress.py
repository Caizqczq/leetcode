"""进度模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Progress(Base):
    """刷题进度"""
    
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), unique=True, nullable=False)
    
    # 状态: not_started / in_progress / mastered
    status = Column(String(20), default="not_started", comment="做题状态")
    
    # 尝试次数
    attempt_count = Column(Integer, default=0, comment="尝试次数")
    
    # 掌握程度（已完成复习轮次）0-5
    mastery_level = Column(Integer, default=0, comment="掌握程度(复习轮次) 0-5")
    
    # 时间记录
    first_solved = Column(DateTime, nullable=True, comment="首次完成时间")
    last_attempt = Column(DateTime, nullable=True, comment="最后尝试时间")
    
    # 关联关系
    problem = relationship("Problem", back_populates="progress")
    review_plans = relationship("ReviewPlan", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress problem_id={self.problem_id} status={self.status}>"
