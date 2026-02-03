"""复习计划模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ReviewPlan(Base):
    """艾宾浩斯复习计划"""
    
    __tablename__ = "review_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("progress.id"), nullable=False)
    
    # 复习安排
    scheduled_date = Column(DateTime, nullable=False, comment="计划复习日期")
    review_round = Column(Integer, default=1, comment="第几轮复习")
    
    # 完成状态
    completed = Column(Boolean, default=False, comment="是否已完成")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    
    # 关联关系
    progress = relationship("Progress", back_populates="review_plans")
    
    def __repr__(self):
        return f"<ReviewPlan progress_id={self.progress_id} round={self.review_round}>"
