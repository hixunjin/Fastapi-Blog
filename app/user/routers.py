from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
from sqlalchemy.orm import Session
from app.user.schemas import UserCreate,InputCode,UserLogin,ResponseUserInfo
from app.db.session import get_db
from app.user.models import User
from app.auth.utils import hash_password,verify_password
from app.auth.vrify_code import generate_code,storage_code_to_redis,send_code,verify_code
from app.auth.jwt import create_access_token,get_current_user
from app.blog.models import Blog




@router.post("/CreateUser")
def CreateUser(create_user:UserCreate,db:Session = Depends(get_db)):

    #检查用户中是否存要加入的数据
    existing = db.query(User).filter(User.username == create_user.username).first()
    if existing:
        raise HTTPException(status_code=400,detail="用户已经存在")

    #对密码加密
    hashed_pwd = hash_password(create_user.password)

    #组织数据
    new_user = User(
        username = create_user.username,
        hashed_password = hashed_pwd,
        email = create_user.email,
        is_active=False

    )

    db.add(new_user)
    db.commit()


    #生成验证码
    code = generate_code()
    storage_code_to_redis(create_user.email, code)
    send_code(create_user.email,code)

    return {"msg": "注册成功，请查收验证码激活账户"}



#用户点击发送验证码，并等到用户输出
@router.post("/activate")
def SendCode(input_code:InputCode,db:Session = Depends(get_db)):
    # 查询用户
    user = db.query(User).filter(User.email == input_code.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 校验验证码

    if not verify_code(input_code.email, input_code.code):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 激活账户
    user.is_active = True
    db.commit()

    return {"msg": "激活成功！现在可以登录了"}












#定义 docs 文档登录验证功能
@router.post('/login')
def login(
        form_data:OAuth2PasswordRequestForm = Depends(),#注入依赖项，获取登录表单数据
        db:Session = Depends(get_db)):
    #根据表单的 username 查询出数据库中的 username
    user = db.query(User).filter(User.username == form_data.username).first()

    # 验证用户名和密码
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="账号或者密码错误！")

    #生成 token
    token = create_access_token({'sub':user.username,"role":"user"})

    # 返回 token 和用户角色
    return {"access_token": token, "token_type": "bearer", "role":"user"}


#登录验证功能接口（JSON 格式，前端可用），下面的登录函数供前端使用
@router.post('/login-json')
def login_json(
        form_data:UserLogin,   #请求体，使用 pydantic 模型接收和校验表单数据
        db:Session = Depends(get_db)):

    #根据表单的 username 查询出数据库中的 username
    user = db.query(User).filter(User.username == form_data.username).first()

    # 验证用户名和密码
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail="账号或者密码错误！")

    #生成 token
    token = create_access_token({'sub':user.username,"role":"user"})

    # 返回 token 和用户角色
    return {"access_token": token, "token_type": "bearer", "role": "user"}




#用户中心,获取数据，返回给前端
@router.get('/GetInfo/{user_id}',response_model=ResponseUserInfo)
def GetInfo(user_id:int,user:User = Depends(get_current_user),db:Session=Depends(get_db)):
    #查询user数据
    user = db.query(User).filter(User.id == user_id).first()

    #最终将查询到的数据构成一个字典，返回给前端
    if not user:
        raise HTTPException(status_code=404,detail="用户信息不存在")

    #查询出对应的博客信息
    blog_list = db.query(Blog).filter(Blog.user_id == user.id).all()
    blogs = [
        {"title": blog.title, "created_at": blog.created_at}
        for blog in blog_list
    ]

    data = {
        'username':user.username,
        'email':user.email,

        #构建标题列表
        'blogs':blogs
    }

    return data


#登录功能
@router.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}