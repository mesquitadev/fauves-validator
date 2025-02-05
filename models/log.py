from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from core.configs import settings

class Log(settings.DBBaseModel):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(String, nullable=True)
    details = Column(String, nullable=True)