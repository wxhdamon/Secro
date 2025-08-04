#/backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def init_db():
    from .models import ScanResult  # 延迟导入，避免循环
    from .base import Base
    Base.metadata.create_all(engine)
