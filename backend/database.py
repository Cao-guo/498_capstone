import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 数据库连接配置
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'Stupid1019!!'
DB_NAME = 'retail_analytics'

# 创建SQLAlchemy实例
db = SQLAlchemy()

def init_db(app: Flask):
    """
    初始化数据库连接
    
    Args:
        app: Flask应用实例
    """
    # 配置SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化SQLAlchemy
    db.init_app(app)

def setup_database():
    """
    检查数据库是否存在，如果不存在则创建数据库和相应的表
    """
    try:
        # 连接到PostgreSQL服务器而不是特定数据库
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 检查数据库是否存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"数据库 {DB_NAME} 不存在，正在创建...")
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            
            # 关闭连接
            cursor.close()
            conn.close()
            
            # 连接到新创建的数据库
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # 从schema.sql文件读取SQL并执行
            script_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                    cursor.execute(sql_script)
                print("已成功创建数据库表结构")
            else:
                print("警告：schema.sql文件不存在，无法创建表")
        else:
            print(f"数据库 {DB_NAME} 已存在")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        # 确保上传目录存在
        upload_dir = os.path.join(os.path.dirname(__file__), 'upload')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"已创建上传目录: {upload_dir}")
            
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise 