
__all__ = ('Member', )

import re

from sqlalchemy import Column, Unicode, Integer, Date, Boolean
from sqlalchemy.orm import validates

from .base_model import BaseModel
from .base_uid import UidModel, IdModel
from configuration import EmailValidationError, PhoneValidationError


class Member(BaseModel, UidModel, IdModel):
    __tablename__ = 'members'
    UID_PREFIX = 'MBR'

    email_regex = re.compile("[^@]+@[^@]+\.[^@]+")
    phone_regex = re.compile("^[+][0-9]{1,3}\s?[0-9]{1,2}[ -/]?[0-9]{6}$")

    crud_metadata = ['uid', 'full_name', 'major', 'email', 'phone', 'birthday', 'graduation', 'paid',
                     'registered', 'student_id', 'ieee_id']

    full_name = Column(Unicode(255), nullable=False)
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
        """
        Validates the provided email against the following regex:
        string@string.string
        where `string` does not contain the '@' sign

        :param key:
        :param email:
        """
        if not re.match(self.email_regex, email):
            raise EmailValidationError("Invalid email {!r}".format(email))
        else:
            return email

    @validates('phone')
    def validate_phone(self, key, phone):
        """
        Validates the provided phone number against the following regex:
        +country_code prefix[ -/]8digit_number
        :param key:
        :param phone:
        """
        if not re.match(self.phone_regex, phone):
            raise PhoneValidationError("Invalid phone number {!r}".format(phone))
        else:
            return phone
