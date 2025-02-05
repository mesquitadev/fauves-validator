from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from core.configs import Settings

Base = declarative_base()

class Ticket(Settings.DBBaseModel):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    email = Column(String, nullable=False)