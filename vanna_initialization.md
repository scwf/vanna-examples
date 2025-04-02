# Vanna初始化指南

Vanna是一个基于RAG和LLM的SQL生成工具，以下是几种常见的初始化方法。

## 安装依赖包

根据不同的需求，可以选择安装不同的依赖包：

### 基础安装
```powershell
pip install vanna
```

### 安装特定数据库支持

#### PostgreSQL支持
```powershell
pip install 'vanna[postgres]'
```

#### DuckDB支持
```powershell
pip install 'vanna[duckdb]'
```

#### SQLite支持（基础包已包含）
```powershell
pip install vanna
```

### 安装本地大语言模型支持

#### OpenAI支持
```powershell
pip install openai
pip install vanna
```

#### Google Gemini支持
```powershell
pip install google-generativeai
pip install vanna
```

#### 安装向量存储支持
```powershell
pip install chromadb
```

### 安装Web界面支持
```powershell
pip install flask
```

### 一次性安装所有常用组件
```powershell
pip install 'vanna[postgres,mysql,flask,chromadb]'
```

## 1. 使用官方提供的远程模型（最简单）

```python
import vanna
from vanna.remote import VannaDefault

# 初始化Vanna，使用远程模型
vn = VannaDefault(model='chinook', api_key=vanna.get_api_key('your_email@example.com'))

# 连接到数据库
vn.connect_to_sqlite('your_database.sqlite')
```

## 2. 使用自定义大语言模型

### 2.1 使用Google Gemini

```python
# 使用Google Gemini作为LLM
from vanna.google.gemini_chat import GoogleGeminiChat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

# 自定义Vanna类
class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config=config)

# 初始化
vn = MyVanna(config={
    'api_key': 'YOUR_GEMINI_API_KEY',
    'model': 'gemini-2.0-flash-lite'
})

# 连接到数据库
vn.connect_to_sqlite('your_database.sqlite')
```

### 2.2 使用OpenAI

```python
# 使用OpenAI作为LLM
from vanna.openai import OpenAI
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

# 自定义Vanna类
class MyVanna(ChromaDB_VectorStore, OpenAI):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI.__init__(self, config=config)

# 初始化
vn = MyVanna(config={
    'api_key': 'YOUR_OPENAI_API_KEY',
    'model': 'gpt-4'  # 或其他支持的模型如 'gpt-3.5-turbo'
})

# 连接到数据库
vn.connect_to_sqlite('your_database.sqlite')
```

### 2.3 使用其他本地模型 (例如 Ollama)

```python
# 使用本地模型作为LLM
from vanna.ollama import Ollama
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

# 自定义Vanna类
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

# 初始化
vn = MyVanna(config={
    'base_url': 'http://localhost:11434',  # Ollama服务地址
    'model': 'llama3'  # 或其他已部署的Ollama模型
})

# 连接到数据库
vn.connect_to_sqlite('your_database.sqlite')
```

## 3. 初始化后的训练

初始化Vanna后，需要进行训练以提高SQL生成质量：

```python
# 训练表结构
vn.train(ddl="""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT
);
""")

# 添加业务术语文档
vn.train(documentation="""
业务定义：客户细分市场包括'企业'、'消费者'和'家庭办公'。
""")

# 添加SQL查询示例
vn.train(sql="""
SELECT customer_name FROM customers WHERE country='中国'
""")
```

## 4. 连接不同类型的数据库

```python
# SQLite
vn.connect_to_sqlite('path_to_database.db')

# PostgreSQL
vn.connect_to_postgres(host='my-host', dbname='my-dbname', 
                      user='my-user', password='my-password', port='my-port')

# 其他数据库需要相应的连接方法
```

## 5. 启动Web界面

```python
from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vn)
app.run()  # 默认在 http://127.0.0.1:5000 启动
```

初始化完成后，您就可以使用 `vn.ask("您的问题")` 来生成SQL查询并获取结果。