__all__ = (
    'User',
)

from sqlalchemy import Column, Unicode
from sqlalchemy.orm import validates

from configuration import EmailValidator, PhoneValidator
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class User(UidModel, IdModel, BaseModel):
    __tablename__ = 'users'
    UID_PREFIX = 'USR'

    crud_metadata = ['email', 'username', 'phone_number', 'first_name', 'last_name', 'uid']

    email = Column(Unicode(255), nullable=True)
    username = Column(Unicode(255), nullable=False)
    phone_number = Column(Unicode(255), nullable=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates('phone_number')
    def validate_phone(self, key, phone):
        return PhoneValidator.validate(phone)
