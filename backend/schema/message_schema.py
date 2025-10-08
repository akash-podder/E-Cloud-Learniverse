from pydantic import BaseModel, ConfigDict

class MessageCreate(BaseModel):
    username: str
    content: str

class MessageUpdate(BaseModel):
    username: str
    content: str

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    content: str