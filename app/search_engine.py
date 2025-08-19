import os
import re
import jieba
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser

# 索引文件目录（存放 Whoosh 索引数据）
INDEX_DIR = "search_index"


#定义 Whoosh 索引结构
schema = Schema(
    id = ID(stored=True,unique=True),

    #分词+搜索
    title = TEXT(stored=True),
    content = TEXT(stored=True),

    #图片URL，用于存储，不用于搜索功能
    image = STORED
)

# ------------------------------
# 初始化索引对象
# ------------------------------
# 如果目录不存在，则创建新索引；如果存在，则打开已有索引
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)
    ix = create_in(INDEX_DIR, schema)  # 创建新索引
else:
    ix = open_dir(INDEX_DIR)           # 打开已有索引


# ------------------------------
# 工具函数：从文章内容提取第一张图片
# ------------------------------
def extract_first_image(content: str) -> str:
    # 匹配 HTML 格式的图片
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if match:
        return match.group(1)

    # 匹配 Markdown 格式的图片
    match = re.search(r'!\[.*?\]\((.*?)\)', content)
    if match:
        return match.group(1)

    return None




#添加更新索引,初始化博客搜索数据或者用户添加博客需要调用这个函数
def add_or_update_blog(
        blog_id:str,
        title:str,
        content:str,
        image:str = None
):

    #这里进行了修改
    # 如果没传 image，就从内容中提取第一张
    if not image:
        image = extract_first_image(content)




    # 获取写入器（Writer）
    writer = ix.writer()



    # 将数据写入索引（使用 update_document 保证同 ID 的记录会被更新）
    writer.update_document(
        id=str(blog_id),
        title=" ".join(jieba.cut(title)),  # 中文分词后再存入
        content=" ".join(jieba.cut(content)),  # 中文分词后再存入
        image=image
    )

    #提交修改
    writer.commit()


def search(keyword: str, page: int = 1, page_size: int = 10):
    """搜索博客"""
    qp = MultifieldParser(["title", "content"], schema=ix.schema)
    q = qp.parse(" ".join(jieba.cut(keyword)))
    results_list = []

    with ix.searcher() as searcher:
        results = searcher.search_page(q, page, pagelen=page_size)
        for hit in results:
            results_list.append({
                "id": hit["id"],
                "title": hit["title"],
                "content": hit["content"][:100],  # 摘要
                "cover_image": hit.get("image")         # 图片 URL
            })
    return results_list







