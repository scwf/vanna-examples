"""
SQLite数据库查看工具

此脚本用于查看SQLite数据库中的表结构和数据内容。
提供了命令行界面，允许用户查询特定表或执行自定义SQL查询。
"""

import os
import sqlite3
import argparse
from tabulate import tabulate

def get_table_names(conn):
    """获取数据库中所有表名"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]

def get_table_schema(conn, table_name):
    """获取表结构"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def view_table_data(conn, table_name, limit=10):
    """查看表数据"""
    cursor = conn.cursor()
    
    # 获取表结构
    schema = get_table_schema(conn, table_name)
    headers = [col[1] for col in schema]
    
    # 查询表数据
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    
    # 打印表头和数据，使用字典格式化并调整对齐方式
    print(f"\n表 '{table_name}' 的数据:")
    tabulate_data = []
    for row in rows:
        # 将数据行转换为字典，以便tabulate能正确处理对齐
        row_dict = {headers[i]: value for i, value in enumerate(row)}
        tabulate_data.append(row_dict)
    
    print(tabulate(tabulate_data, headers="keys", tablefmt="grid", numalign="right", stralign="left"))
    
    # 获取表中的记录总数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"总记录数: {count}，显示了前 {min(limit, count)} 条")

def execute_custom_query(conn, query):
    """执行自定义SQL查询"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # 获取列名
        if cursor.description:
            headers = [col[0] for col in cursor.description]
            
            # 将结果转换为字典列表以便更好地对齐
            dict_rows = []
            for row in rows:
                dict_rows.append({headers[i]: value for i, value in enumerate(row)})
            
            print("\n查询结果:")
            print(tabulate(dict_rows, headers="keys", tablefmt="grid", numalign="right", stralign="left"))
            print(f"返回行数: {len(rows)}")
        else:
            print("查询执行成功，但没有返回数据")
    except sqlite3.Error as e:
        print(f"查询执行失败: {e}")

def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="SQLite数据库查看工具")
    parser.add_argument("--db", default="db\\sales_data.db", help="数据库文件路径")
    parser.add_argument("--table", help="要查看的表名")
    parser.add_argument("--limit", type=int, default=10, help="显示的最大行数")
    parser.add_argument("--query", help="执行自定义SQL查询")
    parser.add_argument("--list-tables", action="store_true", help="列出所有表")
    args = parser.parse_args()
    
    # 检查数据库文件是否存在
    if not os.path.exists(args.db):
        print(f"错误：数据库文件 '{args.db}' 不存在。")
        return
    
    # 连接数据库
    conn = sqlite3.connect(args.db)
    
    try:
        # 列出所有表
        tables = get_table_names(conn)
        
        if args.list_tables:
            print("\n数据库中的表:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
        
        # 查看指定表的数据
        if args.table:
            if args.table in tables:
                view_table_data(conn, args.table, args.limit)
            else:
                print(f"错误：表 '{args.table}' 不存在。")
                print("可用的表:", ", ".join(tables))
        
        # 执行自定义查询
        if args.query:
            execute_custom_query(conn, args.query)
        
        # 如果没有指定操作，显示交互式菜单
        if not (args.list_tables or args.table or args.query):
            while True:
                print("\n\n可用操作:")
                print("1. 列出所有表")
                print("2. 查看表数据")
                print("3. 执行自定义SQL查询")
                print("0. 退出")
                
                choice = input("\n请选择操作 [0-3]: ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    print("\n数据库中的表:")
                    for i, table in enumerate(tables, 1):
                        print(f"{i}. {table}")
                elif choice == "2":
                    if not tables:
                        print("数据库中没有表")
                        continue
                        
                    print("\n可用的表:")
                    for i, table in enumerate(tables, 1):
                        print(f"{i}. {table}")
                    
                    table_choice = input("\n请选择表 [1-{}] 或输入表名: ".format(len(tables))).strip()
                    
                    selected_table = None
                    if table_choice.isdigit() and 1 <= int(table_choice) <= len(tables):
                        selected_table = tables[int(table_choice) - 1]
                    elif table_choice in tables:
                        selected_table = table_choice
                    
                    if selected_table:
                        limit = input("显示的最大行数 [默认10]: ").strip() or "10"
                        if limit.isdigit() and int(limit) > 0:
                            view_table_data(conn, selected_table, int(limit))
                        else:
                            print("无效的行数，使用默认值 10")
                            view_table_data(conn, selected_table, 10)
                    else:
                        print("无效的表选择")
                elif choice == "3":
                    query = input("\n请输入SQL查询:\n").strip()
                    if query:
                        execute_custom_query(conn, query)
                    else:
                        print("查询不能为空")
                else:
                    print("无效的选择，请重试")
    
    finally:
        # 关闭连接
        conn.close()

if __name__ == "__main__":
    print("SQLite数据库查看工具")
    print("=" * 40)
    main() 