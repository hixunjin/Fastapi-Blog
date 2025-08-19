# 从 SQLAlchemy 的 ORM 模块导入 declarative_base 函数
from sqlalchemy.orm import declarative_base


# 创建一个 Base 类，所有 ORM 模型都需要继承它,统一管理所有模型的元信息
Base = declarative_base()
