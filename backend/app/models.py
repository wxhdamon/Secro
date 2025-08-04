#/backend/app/models.py
from sqlalchemy import Column, Integer, JSON, DateTime
from datetime import datetime
from .base import Base  # 引入 Base，而非 db.py，避免循环导入

class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, primary_key=True)
    result = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def save_scan_result(data):
    """保存扫描结果到数据库"""
    from .db import Session  # 延迟导入，避免循环引用
    session = Session()
    try:
        scan = ScanResult(result=data)
        session.add(scan)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
