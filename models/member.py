__all__ = (
    'Member',
)


from sqlalchemy import Column, Unicode, Integer, Date, Boolean
from sqlalchemy.orm import validates

from .base_model import BaseModel
from .base_uid import UidModel, IdModel
from configuration import EmailValidator, PhoneValidator


class Member(BaseModel, UidModel, IdModel):
    __tablename__ = 'members'
    UID_PREFIX = 'MBR'

    crud_metadata = ['uid', 'first_name', 'last_name', 'major', 'email', 'phone', 'birthday', 'graduation', 'paid',
                     'registered', 'student_id', 'ieee_id']

    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    major = Column(Unicode(255), nullable=True)
    email = Column(Unicode(255), nullable=True)
    phone = Column(Unicode(255), nullable=True)
    birthday = Column(Date, nullable=True)
    graduation = Column(Integer, nullable=True)
    paid = Column(Boolean, default=False)
    registered = Column(Boolean, default=False)
    student_id = Column(Boolean, default=False)
    ieee_id = Column(Integer, nullable=True)

    @validates('email')
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates('phone')
    def validate_phone(self, key, phone):
        return PhoneValidator.validate(phone)

