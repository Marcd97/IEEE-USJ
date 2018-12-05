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

    crud_metadata = ['uid', 'name', 'cost', 'members']

    members = relationship('MemberSocietyAssociation', cascade='all,delete')

    name = Column(Unicode(255), unique=True)
    cost = Column(Integer, nullable=False)

    def accept_read_visitor(self, field_names):
        instance_dict = super(Society, self).accept_read_visitor(field_names)
        member_mappings = instance_dict.get('members') or list()
        members = list()
        for member_mapping in member_mappings:
            members.append("{} {}".format(member_mapping.member.first_name, member_mapping.member.last_name))
        instance_dict['members'] = members
        return instance_dict


class MemberSocietyAssociation(BaseModel):
    __tablename__ = 'member_society_assoc'

    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), primary_key=True)
    society_id = Column(Integer, ForeignKey('societies.id', ondelete='CASCADE'), primary_key=True)

    member = relationship('Member')
    society = relationship('Society')
