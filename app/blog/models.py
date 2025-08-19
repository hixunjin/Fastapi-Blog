from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


#定义博客表
class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(200),nullable=False)
    content = Column(Text,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    views = Column(Integer,default=0)
    likes = Column(Integer,default=0)
    cover_image = Column(String(255), nullable=True)

    #下面处理外键关联

    #User表
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    #反向关联
    author = relationship("User",back_populates="blogs")

    #分类表
    categories_id = Column(Integer,ForeignKey('categories.id'),nullable=False)

    #反向关联
    category = relationship("Category",back_populates="blogs")

    #和comment是 一对多
    comments = relationship("Comment",back_populates="blogs")

    #和tags 是多对多关系,需要使用中间表完成关联
    tags = relationship("Tag",back_populates="blogs",secondary="blog_tags")








