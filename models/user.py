from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings
from datetime import datetime

class User(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fullName = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    apiaries = relationship(
        "Apiary",
        back_populates="owner",
        cascade="all,delete-orphan",
        uselist=True,
        lazy="joined"
    )
    meliponaries = relationship(
        "Meliponary",
        back_populates="owner",
        cascade="all,delete-orphan",
        uselist=True,
        lazy="joined"
    )