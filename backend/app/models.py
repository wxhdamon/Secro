#/backend/app/models.py
# 文件：backend/app/models.py
from sqlalchemy import Column, Integer, JSON, DateTime, desc
from datetime import datetime
from .base import Base
from .db import Session

class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, primary_key=True)
    result = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def save_scan_result(data):
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

def load_scan_history(limit=20):
    session = Session()
    try:
        return session.query(ScanResult).order_by(desc(ScanResult.timestamp)).limit(limit).all()
    finally:
        session.close()
