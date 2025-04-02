"""
SQLite数据库初始化脚本

此脚本用于创建和初始化SQLite数据库，包括表结构和示例数据。
"""

import os
import sqlite3

# 确保examples目录存在
os.makedirs("db", exist_ok=True)

# 数据库文件路径
db_path = "db/sales_data.db"

# 如果数据库已存在，则删除
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"已删除旧数据库: {db_path}")

# 连接到数据库（会自动创建文件）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
print("正在创建数据库表...")

# 创建customers表
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    country TEXT,
    segment TEXT
)
""")

# 创建products表
cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL,
    supplier TEXT
)
""")

# 创建orders表
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    product_id INTEGER,
    amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# 插入示例数据
print("正在插入示例数据...")

# 示例customers数据
customers_data = [
    (1, '张三公司', '中国', '企业'),
    (2, '李四商贸', '中国', '企业'),
    (3, '王五', '中国', '消费者'),
    (4, '赵六办公', '中国', '企业'),
    (5, 'ABC Inc', '美国', '企业'),
    (6, 'XYZ Ltd', '英国', '企业'),
    (7, '123 Shop', '日本', '消费者')
]

cursor.executemany("""
INSERT INTO customers (customer_id, customer_name, country, segment)
VALUES (?, ?, ?, ?)
""", customers_data)

# 示例products数据
products_data = [
    (101, '笔记本电脑', '电子产品', 4000.00, '联想'),
    (102, '打印机', '办公设备', 2000.00, '惠普'),
    (103, '办公桌', '家具', 1500.00, '宜家'),
    (104, '办公椅', '家具', 800.00, '宜家')
]

cursor.executemany("""
INSERT INTO products (product_id, product_name, category, price, supplier)
VALUES (?, ?, ?, ?, ?)
""", products_data)

# 示例orders数据
orders_data = [
    (1, 1, '2023-01-15', 101, 5000.00),
    (2, 1, '2023-02-20', 102, 7500.50),
    (3, 2, '2023-01-10', 101, 4200.00),
    (4, 3, '2023-03-05', 103, 1200.75),
    (5, 4, '2023-03-15', 104, 3500.00),
    (6, 5, '2023-02-28', 102, 6500.25),
    (7, 6, '2023-03-10', 103, 8200.00),
    (8, 7, '2023-01-25', 104, 2100.50),
    (9, 5, '2023-04-05', 101, 7200.00),
    (10, 6, '2023-04-15', 102, 5600.75)
]

cursor.executemany("""
INSERT INTO orders (order_id, customer_id, order_date, product_id, amount)
VALUES (?, ?, ?, ?, ?)
""", orders_data)

# 提交事务
conn.commit()

# 验证数据
print("\n验证数据库内容：")

# 查询customers表
cursor.execute("SELECT * FROM customers")
print("\nCustomers表:")
for row in cursor.fetchall():
    print(row)

# 查询products表
cursor.execute("SELECT * FROM products")
print("\nProducts表:")
for row in cursor.fetchall():
    print(row)

# 查询orders表
cursor.execute("SELECT * FROM orders")
print("\nOrders表:")
for row in cursor.fetchall():
    print(row)

# 示例查询：各国家销售总额
cursor.execute("""
SELECT 
    c.country, 
    SUM(o.amount) as total_sales
FROM 
    orders o
JOIN 
    customers c ON o.customer_id = c.customer_id
GROUP BY 
    c.country
ORDER BY 
    total_sales DESC
""")

print("\n各国家销售总额:")
for row in cursor.fetchall():
    print(f"国家: {row[0]}, 销售总额: {row[1]}")

# 示例查询：各产品类别销售额
cursor.execute("""
SELECT 
    p.category, 
    SUM(o.amount) as total_sales,
    COUNT(o.order_id) as order_count
FROM 
    orders o
JOIN 
    products p ON o.product_id = p.product_id
GROUP BY 
    p.category
ORDER BY 
    total_sales DESC
""")

print("\n各产品类别销售额:")
for row in cursor.fetchall():
    print(f"类别: {row[0]}, 销售总额: {row[1]}, 订单数: {row[2]}")

# 关闭连接
conn.close()

print(f"\nSQLite数据库已成功创建和初始化: {db_path}")
print("该数据库包含三个表：customers、products和orders，以及示例数据")
print("现在您可以使用Vanna连接到此数据库进行自然语言查询") 