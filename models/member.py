__all__ = (
    'Member',
)

from app_config.app_config import session
from models.society import MemberSocietyAssociation, Society

from sqlalchemy import Column, Unicode, Integer, Date, Boolean
from sqlalchemy.orm import validates, relationship

from .base_model import BaseModel
from .base_uid import UidModel, IdModel
from configuration import EmailValidator, PhoneValidator


class Member(BaseModel, UidModel, IdModel):
    __tablename__ = 'members'
    UID_PREFIX = 'MBR'

    crud_metadata = ['uid', 'first_name', 'last_name', 'major', 'email', 'phone', 'birthday', 'graduation', 'paid',
                     'registered', 'student_id', 'ieee_id', 'societies']

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

    societies = relationship('MemberSocietyAssociation')

    @validates('email')
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates('phone')
    def validate_phone(self, key, phone):
        return PhoneValidator.validate(phone)

    def accept_write_visitor(self, body):
        societies = body.pop('societies', dict())
        super(Member, self).accept_write_visitor(body)
        for society_uid, belongs in societies.items():
            society = Society.find(society_uid)
            if belongs:
                if MemberSocietyAssociation.query.filter_by(member=self, society=society).one_or_none() is None:
                    session.add(MemberSocietyAssociation(member=self, society=society))
            else:
                association = MemberSocietyAssociation.query.filter_by(member=self, society=society).one_or_none()
                if association is not None:
                    session.delete(association)
        return self

    def accept_read_visitor(self, field_names):
        instance_dict = super(Member, self).accept_read_visitor(field_names)
        society_mappings = instance_dict.get('societies') or list()
        societies = list()
        for society_mapping in society_mappings:
            societies.append(society_mapping.society.name)
        instance_dict['societies'] = societies
        return instance_dict
