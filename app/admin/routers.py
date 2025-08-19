from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.user.schemas import UserLogin,ResponseUserInfo
from app.db.session import get_db
from app.user.models import User
from app.auth.utils import hash_password,verify_password
from app.auth.jwt import create_access_token,get_current_user
from app.blog.models import Blog
from app.admin.schemas import ChangePwd
from fastapi import Query
from typing import List
from typing import Optional


#创建路由器，对应二级路由
router = APIRouter()


#管理员登录函数，表单类型，前端使用
@router.post('/admin/login')
def AdminLogin(
        form_data:OAuth2PasswordRequestForm = Depends(),  #注入依赖项，获取登录表单数据
        db:Session = Depends(get_db)):

    #根据表单的 username 查询出数据库中的 username
    user = db.query(User).filter(User.username == form_data.username).first()

    # 验证用户名和密码
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="账号或者密码错误！")

    if not user.is_admin == 1:
        raise HTTPException(status_code=400,detail="权限不足！")

    #生成 token
    token = create_access_token({'sub':user.username,"role":"admin"})

    # 返回 token 和用户角色
    return {"access_token": token, "token_type": "bearer", "role":"admin"}




#docs文档中的登录功能
@router.post('/login-json')
def login_json(
        form_data:UserLogin,   #请求体，使用 pydantic 模型接收和校验表单数据
        db:Session = Depends(get_db)):
    #根据表单的 username 查询出数据库中的 username
    user = db.query(User).filter(User.username == form_data.username).first()

    # 验证用户名和密码
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="账号或者密码错误！")

    #检查是否为管理员
    if not user.is_admin == 1:
        raise HTTPException(status_code=400,detail="权限不足！")



    #生成 token
    token = create_access_token({'sub':user.username,"role":"admin"})

    # 返回 token 和用户角色
    return {"access_token": token, "token_type": "bearer", "role": "admin"}









#管理员功能:获取User信息，同时加入分页功能

@router.get('/GetAllUserInfo',response_model=List[ResponseUserInfo])
def get_users(
        username: Optional[str] = Query(None, description="用户名，支持模糊搜索"),
        page:int = Query(1,ge=1),      #页码
        page_size:int = Query(10,ge=1,le=100),   #每页数据量
        db:Session = Depends(get_db),
        user:User = Depends(get_current_user),
        ):

        #计算偏移量
        skip = (page - 1) * page_size

        #默认查询出全部数据
        query_users = db.query(User)    #用户数据
        #query_blogs = db.query(Blog)   #博客数据


        #条件过滤
        #根据用户传入的条件进行查询数据，查询条件为:按照用户名去查询，如果不输入查询条件，代表查询所有
        if username:
            #查询出符合条件的用户信息
            query_users = query_users.filter(User.username == username)

            #查询出对应的博客数据
            #query_blogs = query_blogs.filter(Blog.user_id == condition.id)


        #分页处理
        query_users =query_users.order_by(User.created_at.desc()).offset(skip).limit(page_size).all()

        #数据结构的处理
        res_list = []

        #如果只有一个数据,是已经对应好的（但是也可以进行连接查询），如果是多个数据，是不对应的，需要使用连接查询查询出数据
        for user in query_users:
            #处理博客结构，按博客发布时间排序
            blogs = db.query(Blog) \
                .filter(Blog.user_id == user.id) \
                .order_by(Blog.created_at.desc()) \
                .all()


            blogs = [{"id": blog.id,"title": blog.title, "created_at":blog.created_at}
                     for blog in blogs]

            #整理结构
            result = {
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'blogs':blogs   #列表结构
            }

            res_list.append(result)

        return res_list




#管理员功能:修改用户User数据---只修改密码
#直接修改，无需条件
@router.put('/ChangePassword/{user_id}')
def ChangePassword(
        user_id:int,
        input_pwd:ChangePwd,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)
):
    #接收并校验
    user = db.query(User).filter(User.id==user_id).first()


    if not user:
        raise HTTPException(status_code=400,detail="用户不存在！")


    if current_user.is_admin != 1:
        raise HTTPException(status_code=400,detail="权限不足！")


    #对输入的密码加密
    hashed_pwd = hash_password(input_pwd.password)
    user.hashed_password = hashed_pwd
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg":"修改成功！"}



#管理员功能:删除User数据
@router.delete('/DeleteUser/{user_id}')
def DeleteUser(
        user_id:int,
        current_user:User = Depends(get_current_user),
        db:Session = Depends(get_db)
):
    #查询用户
    user = db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=400,detail="用户不存在！")

    #校验权限

    if current_user.is_admin != 1:
        raise HTTPException(status_code=400,detail="权限不足！")


    #删除
    db.delete(user)
    db.commit()
    db.refresh(user)
    return {"msg":"删除成功!"}



#管理员功能:删除博客文章
@router.delete("/DeleteBlog/{blog_id}")
def DeleteBlog(
        blog_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # 查询博客
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=400, detail="博客不存在！")

    # 校验权限
    if current_user.is_admin != 1:
        raise HTTPException(status_code=400, detail="权限不足！")

    # 删除博客
    db.delete(blog)
    db.commit()
    return {"msg": "博客删除成功！"}











