from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base



class User(Base):
    __tablename__ = "users"   # 数据库表名
    id = Column(Integer,primary_key=True,index=True)
    username =Column(String(50),unique=True,index=True,nullable=False)
    avatar = Column(String(255), nullable=True, comment="用户头像URL或路径")
    email = Column(String(100),unique=True,index=True,nullable=False)
    hashed_password = Column(String(128),nullable=False)


    #是否激活,默认没有激活，需要让用户使用邮箱验证码进行激活
    is_active = Column(Boolean,default=False)

    #是否为管理员
    is_admin = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)


    #和文章是一对多关系
    blogs = relationship("Blog",back_populates="author")

    #一对多关系
    comments = relationship("Comment",back_populates="user")


