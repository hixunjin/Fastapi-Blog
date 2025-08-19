import sqlalchemy
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.comments.models import Comment
from app.comments.curd import *
from app.comments.schemas import *
from app.auth.jwt import get_current_user,get_db
from app.user.models import User

router = APIRouter()

#定义工具函数，把数据库中的 Comment 转换为 Pydantic 模型
#其实就是将数据库中的实例转化为字典结构，用于返回响应
def serialize_comment(comment):
    return {
        "id": comment.id,
        "content": comment.content,
        "user": comment.user.username,
        "created_at": comment.created_at,

        #注意，下面有个递归调用，只要检查到一级评论下面有子评论列表，就会调用函数进行字典化，方便前端使用
        #一对多关系访问: comment.replaies
        #更安全的访问方法（核心功能一样）:getattr(comment, "replaies", []) or []
        "replaies": [serialize_comment(reply) for reply in getattr(comment, "replaies", []) or []]
    }


#创建评论接口
@router.post("/",response_model=schemas.CommentResponse)
def Create_comment(
        comment:schemas.CommentCreate,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    #直接调用方法将评论写入数据库
    db_comment = create_comment(db,comment,current_user.id)
    return serialize_comment(db_comment)


#获取一级评论，以及它的子评论
@router.get('/blog/{blog_id}',response_model=List[CommentResponse])
def get_blog_comment(blog_id:int,db:Session = Depends(get_db)):
    #获取所有一级评论
    comments = get_comment_by_blog(db,blog_id)


    #返回一级和二级评论（通过调用工具函数  serialize_comment() 获取二级评论）
    return [
        serialize_comment(c)
        for c in comments
    ]


#删除评论接口

@router.delete('/{comment_id}')
def Delete_comment(
        comment_id:int,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    #调用 curd 方法删除
    db_comment = delete_comment(db,comment_id,current_user.id)

    #如果没有找到或者不是自己的评论，抛出异常
    if not db_comment:
        raise HTTPException(status_code=400,detail="评论不存在或者无权限删除评论")

    return {"msg":"删除成功！"}





