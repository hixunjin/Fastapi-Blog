from fastapi import APIRouter,HTTPException
from app.categories.shcemas import CategoryResponse,UpdateCagegory,CreateCategory
from app.categories.models import Category
from app.auth.jwt import get_db,get_current_user
from fastapi import Depends
from sqlalchemy.orm import Session
from app.user.models import User
from app.blog.models import Blog

router = APIRouter()

#管理员功能，对分类进行增删改查

#增加分类
@router.post('/CreateCategory')
def CreateCategory(
        category:CreateCategory,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):


    #检查下是否为管理员
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403,detail="权限不足！")
    #接收并检查数据
    query = db.query(Category).filter(Category.name == category.name).first()

    if query:
        raise HTTPException(status_code=400,detail="分类已经存在！")


    #添加数据

    data = Category(name=category.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"msg":"添加成功!"}


#修改分类
#根据id进行修改

@router.put('/UpdateCategory/{id}')
def UpdateCategory(
        id:int,
        category:UpdateCagegory,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):


    # 检查下是否为管理员
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="权限不足！")
    # 接收并检查数据是否存在
    get_category = db.query(Category).filter(Category.id == id).first()

    if not get_category:
        raise HTTPException(status_code=400, detail="分类不存在！")


    #更新数据表数据
    get_category.name = category.name
    db.add(get_category)
    db.commit()
    db.refresh(get_category)
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
    get_category = db.query(Category).filter(Category.id == id).first()

    # 检查分类是否存在
    if not get_category:
        raise HTTPException(status_code=404, detail="分类不存在")


    #检查下面是否有关联的博客，如果有，不可以删除
    count = db.query(Blog).filter(Blog.categories_id == id).count()
    if count > 0:
        raise HTTPException(status_code=400,detail="该分类下有博客，无法删除")

    db.delete(get_category)
    db.commit()
    return {"msg":"删除成功!"}




from typing import List
#返回响应，用户使用
@router.get('/categorys',response_model=List[CategoryResponse])
def CateRes(
        db:Session = Depends(get_db),
        ):

    #获取全部的数据,列表+字典结构
    get_category = db.query(Category).all()

    results = []
    for c in get_category:
        data = {
            "id":c.id,
            "name":c.name
        }

        results.append(data)

    return results



























