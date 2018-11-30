__all__ = (
    'Transaction',
)

from sqlalchemy import Column, Unicode, Integer, Date

from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class Transaction(BaseModel, UidModel, IdModel):
    __tablename__ = 'transactions'
    UID_PREFIX = 'TRS'

    crud_metadata = ['uid', 'date', 'amount', 'reason']

    date = Column(Date, nullable=True)
    amount = Column(Integer, nullable=False)
    reason = Column(Unicode(255), nullable=True)


