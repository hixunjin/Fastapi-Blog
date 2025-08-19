import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ==============================
# 将项目根目录加入 sys.path，确保可以导入 app 包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 读取 alembic.ini 配置
config = context.config

# ==============================
# 配置日志，如果 alembic.ini 中配置了日志，fileConfig 会加载
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ==============================
# 导入项目中所有模型，确保 Base.metadata 包含所有表信息
from app.db.base import import_models
import_models()

# 导入 ORM 基类 Base
from app.db.base_class import Base
# target_metadata 告诉 Alembic 哪些表需要进行迁移
target_metadata = Base.metadata

# ==============================
# 离线迁移模式：生成 SQL 脚本，而不直接连接数据库
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,                    # 数据库连接 URL
        target_metadata=target_metadata,  # 元数据，用于自动生成迁移
        literal_binds=True,         # 将绑定参数直接渲染到 SQL
        dialect_opts={"paramstyle": "named"},
    )

    # 开启事务块并执行迁移
    with context.begin_transaction():
        context.run_migrations()

# ==============================
# 在线迁移模式：直接连接数据库执行迁移
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),  # 读取 alembic.ini 配置
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # 不使用连接池
    )

    # 连接数据库
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # 元数据
        )

        # 开启事务并执行迁移
        with context.begin_transaction():
            context.run_migrations()

# ==============================
# 根据 Alembic 当前模式选择运行离线或在线迁移
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
