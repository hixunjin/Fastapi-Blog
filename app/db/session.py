from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# 替换成你的实际 MySQL 配置
DB_USER = "root"
DB_PASSWORD = "As20010504"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "fastapi_blog"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)



#引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖注入，FastAPI 中常用的获取数据库会话的函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
