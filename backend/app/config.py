# backend/app/config.py 

import os

# 优先从 DATABASE_URL 读取
DB_URL = os.getenv("DATABASE_URL")

# 如果没有就使用默认 PostgreSQL 地址
if not DB_URL:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "secro")
    DB_USER = os.getenv("DB_USER", "secro")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "secro")
    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
