from sqlalchemy import Column, Integer, Boolean, String
from database import Base

class Todo(Base):
    __tablename__="todo"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    description=Column(String)
    completed=Column(Boolean, default=False)