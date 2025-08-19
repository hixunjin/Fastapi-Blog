from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from sqlalchemy.sql import func

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer,primary_key=True,index=True)
    content = Column(Text,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    #外键关联
    #用户表
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    user = relationship("User",back_populates="comments")

    #博客表
    blog_id = Column(Integer,ForeignKey("blogs.id"),nullable=False)
    blogs = relationship("Blog",back_populates="comments")

    #评论表，自关联形成一对多，即楼中楼评论
    parent_id = Column(Integer,ForeignKey("comments.id"),nullable=True)
    replaies = relationship("Comment",backref='parent',remote_side=[id],lazy="select",uselist=True)


