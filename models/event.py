__all__ = (
    'Event',
)

from sqlalchemy import Column, Unicode, Date
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Event(BaseModel, UidModel, IdModel):
    __tablename__ = 'events'
    UID_PREFIX = 'EVT'

    crud_metadata = ['uid', 'date', 'location', 'title', 'description']

    date = Column(Date, nullable=True)
    location = Column(Unicode(255), nullable=True)
    title = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=True)
