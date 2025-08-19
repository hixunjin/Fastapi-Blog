"""
评论表
1.查看评论:程序应该返回出一个博客的全部评论
2.评论由用户发起，用户可以删除，用户可以对自己的评论进行回复，这个模块属于博客模块，查询博客内容的时候，连同博客
一同返回出来

"""



from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel


#开始编写模型
#评论基础模型，需要有字段  parent_id ，指定该评论是一级评论而是二级评论，这个字段需要设置默认值为 None
class CommentBase(BaseModel):
    content:str
    parent_id:Optional[int] = None  #父评论id，如果是回复某条评论，则记录这条评论的id


#创建评论模型，以博客为主，创建评论，在评论模型的基础上，必须指定博客id
class CommentCreate(CommentBase):
    blog_id:int   #博客id



#评论返回前端使用的模型
class CommentResponse(BaseModel):
    id:int
    content:str
    created_at: Optional[datetime] = None
    user:str

    #子评论列表,递归调用自身模型
    replaies:List["CommentResponse"] = []


    #允许 pydantic 将 ORM模型直接转换为 pydantic 模型

    class Config:
        orm_mode = True


#下面的代码告诉模型 字符串 "CommentResponse"  是自身模型，方便 pydantic 识别
CommentResponse.update_forward_refs()
























