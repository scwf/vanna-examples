# Vanna自然语言SQL生成器示例

这个项目展示了如何使用Vanna来通过自然语言生成SQL查询，并提供了一个简单的Web界面。

## 项目结构

- `src/start_by_gemini.py`: 使用Google Gemini模型的主程序
- `src/start_by_ollama.py`: 使用本地Ollama模型的主程序
- `src/init_sqlite.py`: 初始化SQLite数据库的脚本
- `src/test_gemini_api.py`: Google Gemini API测试脚本
- `src/start_hello.py`: 简单的Hello World测试脚本

## 前置需求

1. Python 3.8+
2. 安装依赖:
```powershell
pip install 'vanna[flask,chromadb]' google-generativeai sqlalchemy
```

3. 根据选择的模型配置:

   A. 使用Google Gemini:
   - 访问 https://makersuite.google.com/app/apikey 获取API密钥
   - 在代码中配置API密钥

   B. 使用Ollama:
   - 安装Ollama: https://ollama.ai/download
   - 启动Ollama服务
   - 下载模型:
     ```powershell
     ollama pull qwq:32b
     # 或者使用这个轻量级模型
     ollama pull deepseek-r1:8b-llama-distill-q8_0
     ```

## 运行步骤

### 1. 初始化数据库
```powershell
python src/init_sqlite.py
```
这将创建一个包含示例销售数据的SQLite数据库。

### 2. 启动应用

使用Google Gemini:
```powershell
python src/start_by_gemini.py
```

或使用Ollama:
```powershell
python src/start_by_ollama.py
```

## 使用方法

1. 运行启动脚本后，在浏览器中访问 http://127.0.0.1:5000
2. 在界面输入你的自然语言问题，如 "哪个国家的销售额最高？"
3. Vanna会生成SQL查询并执行，然后返回结果

## 示例问题

- 哪个国家的销售额最高？
- 各客户类型的销售情况如何？
- 笔记本电脑的总销售额是多少？
- 2023年各月销售额是多少？
- 哪个客户购买金额最多？

## 数据库结构

### customers表
- customer_id: 客户ID
- customer_name: 客户名称
- country: 国家
- segment: 客户类型（企业/消费者/家庭办公）

### orders表
- order_id: 订单ID
- customer_id: 客户ID（关联customers表）
- order_date: 订单日期
- product_id: 产品ID
- amount: 销售金额

## 产品信息
- 101: 笔记本电脑
- 102: 打印机
- 103: 办公桌
- 104: 办公椅

## Vanna核心概念

Vanna是一个Python包，使用检索增强生成（RAG）和大语言模型（LLM）来帮助生成准确的SQL查询。工作流程分为两步：

1. **训练RAG模型** - `vn.train(...)`
   - 提供表结构信息（DDL语句）
   - 添加业务文档说明
   - 提供SQL查询示例

2. **提问生成SQL** - `vn.ask(...)`
   - 使用参考语料库生成SQL查询
   - 查询数据库并返回结果

## 注意事项

1. 确保网络能够访问相应的服务（Google API或Ollama服务）
2. 如果使用Google Gemini，确保API密钥有效且有足够的配额
3. 如果使用Ollama，确保服务正在运行且模型已下载
4. 首次运行时需要等待模型训练完成