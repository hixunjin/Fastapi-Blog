from pydantic import BaseModel,EmailStr
from  datetime import datetime
from typing import List



#创建用户模型
class UserCreate(BaseModel):
    username:str
    password:str
    email:EmailStr


#登录功能接受模型
class UserLogin(BaseModel):
    username:str
    password:str


#接受模型:修改用户密码，仅仅修改密码
class UpdatePassword(BaseModel):
    old_pwd:str
    new_pwd:str



#用户中心---响应模型:一个模型对应两个数据模型
class TitleInfo(BaseModel):
    title: str
    created_at: datetime

#用户响应模型
class ResponseUserInfo(BaseModel):
    username:str
    email:EmailStr
    blogs:List[TitleInfo]



#增加响应模型（登录成功后返回 token）
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True  # 支持从 SQLAlchemy 对象自动转换



#输入模型
class InputCode(BaseModel):
    email:EmailStr
    code:str

