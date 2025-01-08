from typing import Optional
from pydantic import BaseModel as SCBaseModel
from datetime import datetime

class CreateUserSchema(SCBaseModel):
    fullName: str
    cpf: str
    email: str
    password: str
    phone: str
    role: str

    class Config:
        from_attributes = True


class UserSchema(SCBaseModel):
    id: int
    fullName: str
    cpf: str
    email: str
    phone: str
    role: str
    createdAt: datetime
    updatedAt: Optional[datetime]

    class Config:
        from_attributes = True