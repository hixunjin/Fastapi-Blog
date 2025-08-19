📖 博客系统（基于 FastAPI + MySQL）
🚀 项目简介

本项目是一个基于 FastAPI + MySQL 的博客系统，支持 用户管理、博客文章、标签、分类、评论 等功能。
同时包含 后台管理模块 和 前台用户模块，实现了从用户注册、登录到文章发布、评论、搜索的完整功能。

本系统适合作为 FastAPI 全栈开发的学习项目，涵盖 数据库设计、API 设计、认证授权、Redis 缓存、全文搜索、富文本编辑器集成 等常见开发场景。

📂 项目结构

app/
├── users/           # 用户模块（注册、登录、个人中心）
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes.py
│   └── services.py
│
├── blogs/           # 博客模块（文章发布、编辑、删除、详情）
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes.py
│   └── services.py
│
├── tags/            # 标签模块（多对多关系）
│   ├── ...
│
├── categories/      # 分类模块（文章分类，支持后台管理与用户选择）
│   ├── ...
│
├── comments/        # 评论模块（文章评论，多对一关系）
│   ├── ...
│
├── auth/            # 认证模块（注册、登录、验证码、JWT）
│   ├── routes.py
│   ├── utils.py     # JWT 令牌、密码加密
│   └── email.py     # 邮箱验证码发送
│
├── core/            # 全局配置、安全配置
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── db/              # 数据库初始化、连接配置
│   ├── base.py
│   ├── session.py
│   └── init_db.py
│
└── main.py          # FastAPI 应用启动入口



🗄️ 数据库设计
用户表（User）

存储普通用户与管理员

包含头像字段

与博客表（Blog）一对多

博客表（Blog）

存储用户发布的博客

与用户表多对一

与标签表多对多（通过中间表）

与分类表多对一

与评论表一对多

标签表（Tag）

多对多关系

用于文章的标签管理

分类表（Category）

与博客表一对多

管理员可新增、修改、删除分类

评论表（Comment）

与博客表多对一

存储用户的评论内容

🔑 功能模块
1. 后台管理模块

管理员对用户账号、博客文章的 增删改查

管理员对分类的 增删改查

2. 用户模块

用户注册：邮件验证码激活（验证码存储在 Redis）

用户登录：基于 OAuth2 密码模式 + JWT 令牌

用户中心：展示个人信息、修改密码、查看已发布的文章

3. 首页模块

博客展示：无需登录即可查看

搜索功能：使用 Whoosh + Jieba 分词

分页功能：支持分页浏览文章

4. 博客模块

发布文章（需登录），支持 图片、代码、富文本编辑器（CKEditor）

删除文章

博客详情页：展示完整内容，含浏览量、点赞量、发布时间、评论等

⚙️ 技术栈

后端框架: FastAPI

数据库: MySQL + SQLAlchemy

缓存: Redis（存储验证码）

认证授权: OAuth2 + JWT

搜索引擎: Whoosh + Jieba

富文本编辑器: CKEditor

依赖管理: Poetry / pip + venv
