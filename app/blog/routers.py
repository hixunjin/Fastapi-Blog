import datetime
from fastapi import APIRouter, Query
from app.search_engine import add_or_update_blog,search
from app.blog.schemas import BlogCreate, SearchResponse
from sqlalchemy.orm import Session
from app.blog.schemas import BlogResponses
from app.auth.jwt import get_db,get_current_user
from fastapi import Depends
from  app.blog.models import Blog
from app.user.models import User
from typing import List
from app.blog.schemas import BlogDetailResponse
from fastapi import HTTPException
from app.categories.models import Category
from app.search_engine import add_or_update_blog
from app.blog.schemas import AddBlog
from app.blog.schemas import GetBlogByCategory
from app.blog.schemas import GetBlogByCategory,GetBlogByTag
from app.tags.models import Tag
from app.tags.models import blog_tags




#创建二级路由
router = APIRouter()

#添加博客到索引
@router.post('/add_blog')
def add_blog(blog:BlogCreate):

    #调用工具函数
    add_or_update_blog(blog.blog_id,blog.title,blog.content,blog.image)
    return {"msg":"博客已经添加至索引"}


#搜索功能
@router.get('/search',response_model=SearchResponse)
def search_blogs(
        keyword:str = Query(...,description="请输入搜索关键词"),
        page:int = Query(1,ge=1),
        page_size:int = Query(10,ge=1,le=50)

):
    results = search(keyword,page,page_size)
    return SearchResponse(results = results,total = len(results))




#获取博客列表
@router.get('/GetBlogs',response_model=List[BlogResponses])
def GetBlogs(
        page:int = Query(1,ge=1), #页码
        page_size:int = Query(10,ge=1,le=100), #每页数据量
        db:Session = Depends(get_db),
):

    #计算偏移量
    skip = (page - 1) * page_size

    #没有条件过滤，直接查询出全部的数据，并进行分页处理
    query_blogs = db.query(Blog).order_by(Blog.created_at.desc()).offset(skip).limit(page_size).all()

    #下面开始数据处理
    res_list = []
    for blog in query_blogs:
        #先查询出博客对应的作者和头像,一对一关系，一个博客文章只查询出一个用户信息
        GetUser = db.query(User).filter(User.id == blog.user_id).first()


        #处理数据
        results = {
            #'user':
            "id":blog.id,
            'title':blog.title,
            "created_at":blog.created_at,
            "views":blog.views,
            "likes":blog.likes,
            "author":GetUser.username,
            'avater':GetUser.avatar
        }

        res_list.append(results)



    return res_list





#博客详情页:这个页面是用户点击首页列表的博客或者搜索出来的博客，点击进去显示完整的博客内容
@router.get('/Detail/{blog_id}',response_model=BlogDetailResponse)
def detail(
        blog_id:int,
        db:Session = Depends(get_db),
):
    #查询博客并进行校验
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=400,detail="博客不存在！")

    #数据处理
    #根据博客内容获得作者信息---有博客表到用户表进行查询
    user = db.query(User).filter(User.id == blog.user_id).first()

    #组建信息
    result = {
        'id': blog.id,
        'title': blog.title,
        'content': blog.content,
        'created_at': blog.created_at,
        'views': blog.views,
        'likes': blog.likes,
        'cover_image': blog.cover_image,
        'user': user
    }

    #返回结果
    return result





#创建博客文章
@router.post('/CreateBlog')
def CreateBlog(
        blog:AddBlog,
        current_user:User = Depends(get_current_user),
        db:Session = Depends(get_db)):

    #数据校验
    if not blog.title:
        raise HTTPException(status_code=400,detail="标题必填")
    if not blog.content:
        raise HTTPException(status_code=400,detail="内容必填")
    if not blog.cover_image:
        raise HTTPException(status_code=400,detail="请设置封面图片")
    if not blog.categories_id:
        raise HTTPException(status_code=400,detail="请填写分类id")

    #校验数据库中是否存在该分类
    category = db.query(Category).filter(Category.id == blog.categories_id).first()

    if not category:
        raise HTTPException(status_code=400,detail="分类不存在！")

    #处理数据
    new_blog = Blog(
        title = blog.title,
        content = blog.content,
        created_at = datetime.datetime.utcnow(),  #这个字段不属于 pydantic 模型，而是直接赋值
        user_id = current_user.id,
        categories_id = blog.categories_id,
        cover_image = blog.cover_image,
    )

    #添加到数据库中
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)



    # 处理标签（多对多关系）
    if blog.tags:  # 如果 AddBlog 有 tags 字段

        #用于添加标签
        tag_objs = []
        for tag_name in blog.tags:

            #查询数据库中是否有当前标签，如果没有则创建
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()  # 让 tag.id 生效


            #将标签添加到列表中
            tag_objs.append(tag)
        #将标签赋值给  new_blogs.tags
        new_blog.tags = tag_objs
        db.commit()

    #更新搜索数据
    add_or_update_blog(
        blog_id=str(new_blog.id),
        title=new_blog.title,
        content=new_blog.content,
        image=new_blog.cover_image
    )

    return {"msg":"创建成功!"}



#用户删除自己发布的文章
@router.delete('/delete/{blog_id}')
def DeleteBlog(
        blog_id:int,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)  #这里是当前用户，含有用户信息，本质就是User实例，可以直接使用
):

    #首先判断下当前博客是不是和当前用户对应
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    #检查下博客是否存在
    if not blog:
        raise HTTPException(status_code=404, detail="博客不存在")

    #校验是否为其它用户的博客文章
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=400,detail="无法删除其他用户博客！")


    #删除
    db.delete(blog)
    db.commit()
    return {"msg":"删除成功!"}




#按照分类进行查询博客信息
@router.get('/GetBlogByCategory',response_model=List[GetBlogByCategory])
def GetBlogByCategory(
        #不需要登录和身份验证，只需要对数据库进行查询操作，并对数据进行处理
        db:Session = Depends(get_db)):

    #获取全部分类数据
    categories = db.query(Category).all()

    results = []

    #关系是 一对多
    for c in categories:
        #根据分类 categories_id  查询出对应的博客文章
        blogs = db.query(Blog).filter(Blog.categories_id == c.id).all()

        #组织数据,使用的是列表表达式
        blogs_data = [
            {
                'id':b.id,
                'title':b.title,
                'content':b.content,
                'cover_image':b.cover_image
            }
        for b in blogs

        ]

        #数据组织

        results.append(
            {
                'id':c.id,
                'name':c.name,
                'blogs':blogs_data    #这里是博客列表数据
            }
        )

    return results




#按照标签进行查询博客
@router.get('/GetBlogByTag',response_model=List[GetBlogByTag])
def GetBlogByTag(
        #不需要登录和身份验证，只需要对数据库进行查询操作，并对数据进行处理
        db:Session = Depends(get_db)):

    #既然是按照分类进行获取博客集合数据，那么就以博客数据为主

    #获取全部分类数据
    tags = db.query(Tag).all()

    results = []


    #for循环categories，同时查询出对应的博客数据，并进行数据处理
    #关系是 一对多
    for tag in tags:
        #根据分类 categories_id  查询出对应的博客文章
        blogs = db.query(Blog).join(blog_tags).filter(blog_tags.c.tag_id == tag.id).all()



        #组织数据,使用的是列表表达式
        blogs_data = [
            {
                'id':b.id,
                'title':b.title,
                'content':b.content,
                'cover_image':b.cover_image
            }
        for b in blogs

        ]

        #将处理好的列表博客数据添加到分类信息的博客字段

        results.append(
            {
                'id':tag.id,
                'name':tag.name,
                'blogs':blogs_data    #这里是博客列表数据
            }
        )

    return results


