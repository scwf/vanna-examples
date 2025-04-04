"""
使用Vanna启动Web应用示例

此示例展示如何初始化Vanna并启动Web界面，
让用户通过浏览器使用自然语言查询数据库。
使用本地SQLite数据库作为轻量级解决方案。
使用DeepSeek作为大语言模型。
"""

import pandas as pd
import os
import sys
import configparser
from pathlib import Path
from vanna.deepseek.deepseek_chat import DeepSeekChat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp

# 从配置文件读取API密钥
def read_config():
    config_paths = [
        './mykey.config',
        '../mykey.config',
        Path(os.path.abspath(__file__)).parent.parent / 'mykey.config'
    ]
    
    config = configparser.ConfigParser()
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                # 明确指定使用UTF-8编码读取配置文件
                with open(config_path, 'r', encoding='utf-8') as f:
                    config.read_file(f)
                print(f"已从 {config_path} 加载配置")
                if 'DEEPSEEK' in config and 'API_KEY' in config['DEEPSEEK']:
                    return config['DEEPSEEK']['API_KEY']
            except Exception as e:
                print(f"读取配置文件 {config_path} 失败: {e}")
    
    return None

# 获取API密钥
api_key = read_config()
if not api_key:
    print("错误: 未找到DeepSeek API密钥")
    print("请创建mykey.config文件并添加以下内容:")
    print("[DEEPSEEK]")
    print("API_KEY=你的密钥")
    sys.exit(1)

# 初始化Vanna
class MyVanna(ChromaDB_VectorStore, DeepSeekChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        DeepSeekChat.__init__(self, config=config)

# 配置API密钥和模型
vn = MyVanna(config={
    'api_key': api_key,  # 从配置文件读取API密钥
    'model': 'deepseek-chat'  # 使用DeepSeek的模型
})

# 数据库文件路径
db_path = os.path.abspath("db\\sales_data.db")

# 检查数据库是否存在
if not os.path.exists(db_path):
    print(f"错误：数据库文件 {db_path} 不存在。")
    print("请先运行 'python db\\init_sqlite.py' 创建数据库。")
    exit(1)

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

print("训练完成，所有数据准备就绪！")

# 启动Flask应用
if __name__ == "__main__":
    print("启动Vanna Web应用界面...")
    print("试试问这些问题:")
    print("1. 哪个国家的销售额最高？")
    print("2. 各客户类型的销售情况如何？")
    print("3. 笔记本电脑的总销售额是多少？")
    app = VannaFlaskApp(vn)
    app.run()