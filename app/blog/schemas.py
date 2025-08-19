from  datetime import datetime
from pydantic import BaseModel
from typing import List,Optional

#更新搜索数据，用户添加数据时调用这个函数
class BlogCreate(BaseModel):
    """id title content"""
    id:int
    title:str
    content:str
    image:Optional[str] = None   #图片URL，可选



#搜索结果
class BlogSearchResult(BaseModel):
    id:int
    title:str
    content:str
    image:Optional[str] = None   #图片URL，可选


#搜索结果，列表
class SearchResponse(BaseModel):
    results:List[BlogSearchResult]
    total:int



#作者信息
class UserInfo(BaseModel):
    username:str
    avatar:Optional[str] = None


#博客:id title created_at views likes
class BlogResponses(BaseModel):
    id:int
    title:str
    created_at:datetime
    views:Optional[int] = None
    likes:Optional[int] = None
    author:str
    avatar: Optional[str] = None



#博客详情页
#返回的模型，以博客为主要信息，附带作者信息
class BlogDetailResponse(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime
    views: Optional[int] = None
    likes: Optional[int] = None
    cover_image:Optional[str] = None   #图片为路径地址，是字符串类型
    user:UserInfo




#1.发布文章（需要登录）:发布的内容中允许包含 图片 、代码，内嵌一个富文本编辑器，比如：ckeditor
class AddBlog(BaseModel):
    title:str
    content:str
    cover_image:str
    categories_id: int
    tags: Optional[List[str]] = []  # 标签 ID 列表


#博客信息，嵌套在分类数据模型中
class BlogListResponse(BaseModel):
    id:int
    title:str
    content:str
    cover_image:Optional[str] = None



#返回数据需要的信息
class GetBlogByCategory(BaseModel):
    id:int
    name:str
    blogs:List[BlogListResponse]



#通过标签获取信息
class GetBlogByTag(BaseModel):
    id:int
    name:str
    blogs:List[BlogListResponse]

