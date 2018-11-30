from sqlalchemy import Column, Unicode, Integer, ForeignKey , Date
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Meeting(UidModel,IdModel,BaseModel):
    __tablename__='Meeting'
    Date=Column(Date , nullable=False)
    Location=Column(Unicode(255),nullable=False)
    Title=Column(Unicode(255),nullable=False)
    Description=Column(Unicode(255),nullable=False)
    Priority=Column(Integer,nullable=False)
    Requested_members=Column(Integer,nullable=False)


class UserMeetingAssociation(BaseModel,UidModel,IdModel):
    __tablename__='UserMeeting'
    meeting_id=Column(Integer,ForeignKey('meeting.id',ondelete='CASCADE'),nullable=False)
    user_id=Column(Integer,ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=relationship('User')
    meeting=relationship('Meeting')