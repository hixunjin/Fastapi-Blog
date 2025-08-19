from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from .user import routers as APIUser
from app.admin import routers as APIAdmin
from app.blog import routers as APIBlog
from app.categories import  routers as APICategory
from app.tags import routers as APITag
from app.db.base import import_models  # 确保引入
import os
from fastapi.responses import FileResponse
from app.comments import routers as APIComment
import_models()  # 提前加载所有模型，防止关系无法解析


#创建一级路由
app = FastAPI()


#接口地址
app.include_router(APIUser.router, prefix="/api/users", tags=["用户接口列表"])
app.include_router(APIAdmin.router, prefix="/api/admin", tags=["管理员接口列表"])
app.include_router(APIBlog.router, prefix="/api/blog", tags=["博客接口列表"])
app.include_router(APICategory.router, prefix="/api/category", tags=["分类接口列表"])
app.include_router(APITag.router, prefix="/api/tag", tags=["标签接口列表"])
app.include_router(APIComment.router, prefix="/api/comment", tags=["评论接口列表"])

