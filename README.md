# Vanna自然语言SQL生成器示例

这个项目展示了如何使用Vanna来通过自然语言生成SQL查询，并提供了一个简单的Web界面。

## 项目结构

- `src/start_by_gemini.py`: 使用Google Gemini模型的主程序
- `src/start_by_deepseek.py`: 使用DeepSeek模型的主程序
- `src/start_by_ollama.py`: 使用本地Ollama模型的主程序
- `src/init_sqlite.py`: 初始化SQLite数据库的脚本
- `src/view_sqlite_data.py`: 查看SQLite数据库中表数据的工具
- `src/test_gemini_api.py`: Google Gemini API测试脚本
- `src/start_hello.py`: 简单的Hello World测试脚本
- `mykey.config`: API密钥配置文件（需自行创建）

## 前置需求

1. Python 3.8+
2. 安装依赖:
```powershell
pip install 'vanna[flask,chromadb]' google-generativeai sqlalchemy
pip install openai
pip install tabulate
```

3. 配置API密钥:
   创建`mykey.config`文件，添加以下内容：
   ```ini
   # 使用纯ASCII字符，避免编码问题
   [DEEPSEEK]
   API_KEY=your_deepseek_api_key_here
   
   [GEMINI]
   API_KEY=your_gemini_api_key_here
   ```
   将占位符替换为实际的API密钥。
   
   **注意**: 在Windows系统上，请确保使用UTF-8编码保存配置文件，或者仅使用纯ASCII字符，避免中文等字符导致编码问题。

4. 根据选择的模型配置:

   A. 使用Google Gemini:
   - 访问 https://makersuite.google.com/app/apikey 获取API密钥
   - 添加到配置文件中

   B. 使用DeepSeek:
   - 访问 https://platform.deepseek.com/ 注册并获取API密钥
   - 添加到配置文件中

   C. 使用Ollama:
   - 安装Ollama: https://ollama.ai/download
   - 启动Ollama服务
   - 下载模型:
     ```powershell
     ollama pull qwq:32b
     # 或者使用这个轻量级模型，推荐本地使用gemma3的12b模型
     ollama pull gemma3:12b
     ```

## 运行步骤

### 1. 初始化数据库
```powershell
python src\init_sqlite.py
```
这将创建一个包含示例销售数据的SQLite数据库。

### 2. 启动应用

使用Google Gemini:
```powershell
python src\start_by_gemini.py
```

使用DeepSeek:
```powershell
python src\start_by_deepseek.py
```

或使用Ollama:
```powershell
python src\start_by_ollama.py
```

### 3. 查看数据库内容(可选)
```powershell
python src\view_sqlite_data.py
```
这是一个交互式工具，允许你浏览数据库中的表和数据。

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

### products表
- product_id: 产品ID
- product_name: 产品名称
- category: 产品类别
- price: 价格
- supplier: 供应商

### orders表
- order_id: 订单ID
- customer_id: 客户ID（关联customers表）
- order_date: 订单日期
- product_id: 产品ID（关联products表）
- amount: 销售金额

## 产品信息
- 101: 笔记本电脑
- 102: 打印机
- 103: 办公桌
- 104: 办公椅

## 各模型比较

### Google Gemini
- 优点：响应速度快，生成SQL准确性高
- 缺点：需要Google API密钥，有API调用限制

### DeepSeek
- 优点：中文处理能力强，支持复杂查询
- 缺点：需要DeepSeek API密钥，可能有API调用限制
- 适用场景：需要处理中文自然语言查询的应用

### Ollama (本地模型)
- 优点：本地运行，无需网络连接，无API调用限制
- 缺点：需要较高的系统资源，生成速度相对较慢
- 适用场景：对数据隐私要求高的环境

## Vanna核心概念

Vanna是一个Python包，使用检索增强生成（RAG）和大语言模型（LLM）来帮助生成准确的SQL查询。工作流程分为两步：

1. **训练RAG模型** - `vn.train(...)`
   - 提供表结构信息（DDL语句）
   - 添加业务文档说明
   - 提供SQL查询示例

2. **提问生成SQL** - `vn.ask(...)`
   - 使用参考语料库生成SQL查询
   - 查询数据库并返回结果

## 常见问题解决

### 配置文件编码问题
如果遇到如下错误：
```
读取配置文件 mykey.config 失败: 'gbk' codec can't decode byte 0xac in position 59: illegal multibyte sequence
```
这是因为Windows默认使用GBK编码而不是UTF-8编码。解决方法：
1. 使用记事本打开配置文件，选择"另存为"，在编码下拉框中选择"UTF-8"格式保存
2. 或者简化配置文件，只使用ASCII字符，避免中文注释

## 注意事项

1. 确保网络能够访问相应的服务（Google API、DeepSeek API或Ollama服务）
2. API密钥保存在`mykey.config`文件中，该文件不应提交到版本控制系统
3. 如果API密钥不正确或过期，程序会在启动时提示错误
4. 如果使用Ollama，确保服务正在运行且模型已下载
5. 首次运行时需要等待模型训练完成
6. DeepSeek模型对中文支持较好，适合处理中文自然语言查询