from pydantic import BaseModel

#修改用户密码模型
class ChangePwd(BaseModel):
    password:str




