from pydantic import BaseModel


#管理员使用---创建标签
class CreateTag(BaseModel):
    name:str


#响应模型，用户使用，需要用到 name 、id
class TagResponse(BaseModel):
    id:int
    name:str


#修改标签
class UpdateTag(BaseModel):
    name:str