from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.orm import relationship,sessionmaker,scoped_session
from datetime import datetime
import os

# Create a source for sqlalchemy

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

connection_str= "sqlite:///" + os.path.join(BASE_DIR,'tasks.db')


Base=declarative_base()



engine=create_engine(connection_str,echo=True)


session=scoped_session(
    sessionmaker(bind=engine)
)

Base.query = session.query_property()


"""
table users:
id - primary key
username : str
email


table task:
id - primary key
title : str
description:str
time: datetime

"""
# User model
class User(Base):
    __tablename__="users"
    id=Column(Integer(),primary_key=True)
    username=Column(String(45),nullable=False)
    email=Column(String(80),nullable=False)
    task=relationship("Task",backref="user")


    def __repr__(self):
        return f"<User {self.username}>"


# Task Model
class Task(Base):
    __tablename__="tasks"
    id=Column(Integer(),primary_key=True)
    title=Column(String(100),nullable=False)
    description=Column(Text(),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id=Column(Integer(),ForeignKey("users.id"))

    def __repr__(self):
        return f"<Task {self.title}>"

