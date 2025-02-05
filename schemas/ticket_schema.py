from pydantic import BaseModel as SCBaseModel


class TicketCreateSchema(SCBaseModel):
    user_id: str
    email: str


class TicketSchema(TicketCreateSchema):
    id: int

    class Config:
        orm_mode = True
