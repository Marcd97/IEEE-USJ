__all__ = (
    'Society',
    'MemberSocietyAssociation',
)

from sqlalchemy import Column, Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Society(BaseModel, UidModel, IdModel):
    __tablename__ = 'societies'
    UID_PREFIX = 'SCT'

    crud_metadata = ['uid', 'name', 'cost']

    members = relationship('MemberSocietyAssociation', cascade='all,delete')

    name = Column(Unicode(255), unique=True)
    cost = Column(Integer, nullable=False)


class MemberSocietyAssociation(BaseModel):
    __tablename__ = 'member_society_assoc'

    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), primary_key=True)
    society_id = Column(Integer, ForeignKey('societies.id', ondelete='CASCADE'), primary_key=True)

    member = relationship('Member')
    society = relationship('Society')
