__all__ = (
    'Meeting',
    'UserMeetingAssociation',
)

from sqlalchemy import Column, Unicode, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.user import User
from .base_model import BaseModel
from .base_uid import UidModel, IdModel
from app_config.app_config import session


class Meeting(UidModel, IdModel, BaseModel):
    __tablename__ = 'meetings'
    UID_PREFIX = 'MTG'

    crud_metadata = ['uid', 'date', 'location', 'title', 'description', 'priority', 'requested_users']

    date = Column(Date, nullable=True)
    location = Column(Unicode(255), nullable=True)
    title = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=True)
    priority = Column(Integer, default=0)
    requested_users = relationship('UserMeetingAssociation', cascade='all,delete')

    def accept_write_visitor(self, body):
        requested_users = body.pop('requested_users', dict())
        super(Meeting, self).accept_write_visitor(body)
        for user_uid, belongs in requested_users.items():
            user = User.find(user_uid)
            if belongs:
                if UserMeetingAssociation.query.filter_by(meeting=self, user=user).one_or_none() is None:
                    session.add(UserMeetingAssociation(meeting=self, user=user))
            else:
                association = UserMeetingAssociation.query.filter_by(meeting=self, user=user).one_or_none()
                if association is not None:
                    session.delete(association)
        return self

    def accept_read_visitor(self, field_names):
        instance_dict = super(Meeting, self).accept_read_visitor(field_names)
        user_mappings = instance_dict.get('requested_users') or list()
        requested_users = list()
        for user_mapping in user_mappings:
            requested_users.append("{} {}".format(user_mapping.user.first_name, user_mapping.user.last_name))
        instance_dict['requested_users'] = requested_users
        return instance_dict


class UserMeetingAssociation(BaseModel):
    __tablename__ = 'user_meeting_assoc'
    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    user = relationship('User')
    meeting = relationship('Meeting')
