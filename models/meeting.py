from sqlalchemy import Column, Unicode, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Meeting(UidModel, IdModel, BaseModel):
    __tablename__ = 'meetings'
    UID_PREFIX = 'MTG'
    date = Column(Date, nullable=False)
    location = Column(Unicode(255), nullable=False)
    title = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    priority = Column(Integer, nullable=False)
    requested_users = relationship('UserMeetingAssociation', cascade='all,delete')


class UserMeetingAssociation(BaseModel):
    __tablename__ = 'user_meeting_assoc'
    meeting_id = Column(Integer, ForeignKey('meeting.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    meeting = relationship('Meeting')
