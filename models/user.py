from sqlalchemy import Column, Unicode, Integer, ForeignKey , String
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .base_uid import UidModel, IdModel

class User(UidModel,IdModel,BaseModel):
    __tablename__ = 'User'
    email=Column(String(20),nullable=True)
    username=Column(String(20),nullabe=False)
    phonenumber=Column(Integer,nullable=True)
