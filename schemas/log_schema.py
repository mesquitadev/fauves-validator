from pydantic import BaseModel as SCBaseModel
from datetime import datetime

class LogSchema(SCBaseModel):
    id: int
    event: str
    timestamp: datetime
    user_id: str = None
    details: str = None

    class Config:
        orm_mode = True