from pydantic import BaseModel

class MessageCreate(BaseModel):
    username: str
    content: str

class MessageRead(BaseModel):
    id: int
    username: str
    content: str

    class Config:
        orm_mode = True