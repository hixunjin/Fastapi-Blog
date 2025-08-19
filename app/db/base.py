from app.db.base_class import Base  # 从 base_class 导入 Base，这是所有 SQLAlchemy 模型的基类

#定义一个函数，用于延迟导入所有模型
def import_models():
    import app.user.models
    import app.blog.models
    import app.comments.models
    import app.tags.models
    import app.categories.models
