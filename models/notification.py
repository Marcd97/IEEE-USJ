__all__ = (
    'Notification',
)

from datetime import date
from sqlalchemy import Column, Unicode, Integer, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from models.user import User

from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Notification(UidModel, IdModel, BaseModel):
    __tablename__ = 'notifications'
    UID_PREFIX = 'NTF'

    crud_metadata = ['message', 'acknowledged', 'date', 'uid']

    target = relationship('User', cascade='all,delete')

    target_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    message = Column(Unicode(255), nullable=False)
    acknowledged = Column(Boolean, default=False)
    date = Column(Date, nullable=False)

    def accept_write_visitor(self, body):
        try:
            body.pop('date')
        except KeyError:
            pass
        else:
            raise Exception()

        target_uid = body.pop('target_uid')
        super(Notification, self).accept_write_visitor(body)

        self.date = date.today()

        target = User.find(target_uid)
        self.target = target
        return self
