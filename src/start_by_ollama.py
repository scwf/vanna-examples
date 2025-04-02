"""
使用Vanna启动Web应用示例 (Ollama版)

此示例展示如何初始化Vanna并启动Web界面，
让用户通过浏览器使用自然语言查询数据库。
使用本地SQLite数据库作为轻量级解决方案。
使用Ollama本地大语言模型作为生成引擎。
"""

import pandas as pd
import os
from vanna.ollama import Ollama
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp

# 初始化Vanna
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

# 配置Ollama模型
vn = MyVanna(config={
    'base_url': 'http://localhost:11434',  # Ollama服务地址，确保已启动Ollama服务
    # 'model': 'qwq:32b'  # 使用qwq-32b模型
    # 'model': 'deepseek-r1:8b-llama-distill-fp16'  # 使用deepseek蒸馏版
    'model': 'gemma3:12b'  # gemma3-12b模型

})

# 数据库文件路径
db_path = os.path.abspath("db/sales_data.db")

# 检查数据库是否存在
if not os.path.exists(db_path):
    print(f"错误：数据库文件 {db_path} 不存在。")
    print("请先运行 'python src/init_sqlite.py' 创建数据库。")
    exit(1)

# 连接到SQLite数据库
vn.connect_to_sqlite(db_path)

print("正在训练Vanna模型...")

# 提供训练数据
# 1. 表结构信息
vn.train(ddl="""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    country TEXT,
    segment TEXT
);
         
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL,
    supplier TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    product_id INTEGER,
    amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# 2. 业务术语文档
vn.train(documentation="""
我们的客户细分市场(segment)包括'企业'、'消费者'。
销售金额(amount)以人民币计算，是指的商品销售的金额，而不是商品销售的数量。
产品ID(product_id)对应的产品为：101=笔记本电脑, 102=打印机, 103=办公桌, 104=办公椅。
""")

# 3. SQL查询示例
# vn.train(sql="""
# SELECT 
#     c.country, 
#     SUM(o.amount) as total_sales
# FROM 
#     orders o
# JOIN 
#     customers c ON o.customer_id = c.customer_id
# GROUP BY 
#     c.country
# ORDER BY 
#     total_sales DESC
# """)

# vn.train(sql="""
# SELECT 
#     p.category, 
#     SUM(o.amount) as total_sales,
#     COUNT(o.order_id) as order_count
# FROM 
#     orders o
# JOIN 
#     products p ON o.product_id = p.product_id
# GROUP BY 
#     p.category
# ORDER BY 
#     total_sales DESC
# """)

print("训练完成，所有数据准备就绪！")

# 启动Flask应用
if __name__ == "__main__":
    print("启动Vanna Web应用界面（Ollama版）...")
    print("请确保Ollama服务已在本地运行 (http://localhost:11434)")
    print("请在浏览器中访问: http://127.0.0.1:5000")
    print("试试问这些问题:")
    print("1. 哪个国家的销售额最高？")
    print("2. 各产品类别销售额情况")
    print("3. 笔记本电脑的总销售额是多少？")
    app = VannaFlaskApp(vn)
    app.run()