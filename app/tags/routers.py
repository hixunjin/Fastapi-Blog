from fastapi import APIRouter,HTTPException
from app.auth.jwt import get_db,get_current_user
from fastapi import Depends
from sqlalchemy.orm import Session
from app.user.models import User
from app.tags.schemas import TagResponse,CreateTag,UpdateTag
from app.tags.models import Tag
from app.tags.models import blog_tags
from typing import List


router = APIRouter()


#增加标签
@router.post('/CreateTag')
def CreateTag(
        tag:CreateTag,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):

    #检查下是否为管理员
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403,detail="权限不足！")

    #接收并检查数据
    query = db.query(Tag).filter(Tag.name == tag.name).first()

    if query:
        raise HTTPException(status_code=400,detail="分类已经存在！")


    #添加数据

    data = Tag(name=tag.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"msg":"添加成功!"}


#修改分类，根据id进行修改
@router.put('/UpdateTag/{id}')
def UpdateTag(
        id:int,
        tag:UpdateTag,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):


    # 检查下是否为管理员
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="权限不足！")

    #检查下数据库中是否存在即将要修改的标签记录
    get_tag = db.query(Tag).filter(Tag.id == id).first()
    if not get_tag:
        raise HTTPException(status_code=400, detail="标签不存在！")

    get_tag.name = tag.name
    db.add(get_tag)
    db.commit()
    db.refresh(get_tag)
    return {"msg":"修改成功!"}


#根据id删除分类
@router.delete('/Delete/{id}')
def Delete(
        id:int,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):


    # 检查下是否为管理员
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="权限不足！")

    # 接收并检查数据
    get_tag = db.query(Tag).filter(Tag.id == id).first()
    if not get_tag:
        raise HTTPException(status_code=404, detail="标签不存在")


    #检查下面是否有关联的博客，如果有，不可以删除
    count = db.query(blog_tags).filter(blog_tags.c.tag_id == id).count()
    if count > 0:
        raise HTTPException(status_code=400, detail="该标签已被博客使用，无法删除")


    db.delete(get_tag)
    db.commit()
    return {"msg":"删除成功!"}



#返回响应，用户使用，将标签以列表嵌套字典的形式返回




@router.get('/categorys',response_model=List[TagResponse])
def TagResponses(
        db:Session = Depends(get_db),
        ):

    #获取全部的数据,列表+字典结构
    tag = db.query(Tag).all()

    results = []
    for t in tag:
        data = {
            "id":t.id,
            "name":t.name
        }

        results.append(data)

    return results

