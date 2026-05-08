from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
