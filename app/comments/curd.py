"""
curd文件是对数据库完成增删改查操作，编写好功能函数，供路径操作函数使用
这里是完成对评论数据表的增删查操作，方便路径操作函数直接调用
"""
from sqlalchemy.orm import Session
from app.comments import models,schemas

#创建评论函数
def create_comment(db:Session,comment:schemas.CommentCreate,user_id:int):
    #构造数据库实例，用于添加数据
    db_comment = models.Comment(
        content = comment.content,
        blog_id = comment.blog_id,  #属于哪个博客id
        parent_id=comment.parent_id if comment.parent_id else None,  # 顶层评论存 None, #如果是回复，传入父评论id，否则为 None
        user_id = user_id   #评论发布者
    )

    #添加到数据库中
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


#获取博客的一级评论，不包含回复
def get_comment_by_blog(db:Session,blog_id:int):
    return db.query(models.Comment).filter(
        models.Comment.blog_id == blog_id,
        models.Comment.parent_id == None    #只要一级评论
    ).all()


#删除评论,只能自己删除自己的评论
def delete_comment(db:Session,comment_id:int,user_id:int):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.user_id == user_id
    ).first()

    # 先备份数据
    deleted_comment = {
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id
    }

    #如果存在，则删除
    if comment:
        db.delete(comment)
        db.commit()

    #返回被删除的评论对象
    return deleted_comment



