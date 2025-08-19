from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey,Table
from sqlalchemy.orm import relationship
from app.db.base import Base

#中间表
blog_tags = Table(
    "blog_tags",
    Base.metadata,
    Column('blog_id',Integer,ForeignKey("blogs.id"),primary_key=True),
    Column('tag_id', Integer, ForeignKey("tags.id"), primary_key=True)


)


#Tag模型
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),unique=True,nullable=False)

    #和Blog表关联
    blogs = relationship("Blog",back_populates="tags",secondary=blog_tags)





