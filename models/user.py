from sqlalchemy import Column, Unicode
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class User(UidModel, IdModel, BaseModel):
    __tablename__ = 'users'
    UID_PREFIX = 'USR'

    email = Column(Unicode(255), nullable=True)
    username = Column(Unicode(255), nullabe=False)
    phone_number = Column(Unicode(255), nullable=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
