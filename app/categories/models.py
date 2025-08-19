from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

#分类模型
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)

    #关联表
    blogs = relationship("Blog",back_populates="category")
