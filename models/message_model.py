from sqlalchemy import Column, Integer, String, Text
from database.database_init import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)