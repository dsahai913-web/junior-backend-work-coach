from datetime import datetime
from sqlalchemy import Column,DateTime,String,Text,Integer,ForeignKey
from core.database import Base

class Task(Base):
    __tablename__="task"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    title=Column(String,nullable=False)
    description=Column(Text,nullable=False)
    idempotency_key=Column(String,nullable=True,unique=True,index=True)
    ai_explanation=Column(Text,nullable=True)
    ai_status=Column(String,default="pending",nullable=False)
    status=Column(String,default="pending",nullable=False)
    priority=Column(String,default="medium",nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
