from pydantic import BaseModel

#创建分类
class CreateCategory(BaseModel):
    name:str



#修改分类
class UpdateCagegory(BaseModel):
    name:str


#用户模型，返回出id和name，供前端模板标签 select 使用，然后用户创建博客文章的时候选择一个分类，提交到后端
class CategoryResponse(BaseModel):
    id:int
    name:str

