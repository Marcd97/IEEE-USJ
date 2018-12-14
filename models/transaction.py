__all__ = (
    'Transaction',
)

from sqlalchemy import Column, Unicode, Integer, Date

from .base_model import BaseModel
from .base_uid import UidModel, IdModel
from app_config.app_config import session
from configuration.exceptions import ForcedBalanceError


class Transaction(BaseModel, UidModel, IdModel):
    __tablename__ = 'transactions'
    UID_PREFIX = 'TRS'

    crud_metadata = ['uid', 'date', 'amount', 'reason', 'balance']

    date = Column(Date, nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    amount = Column(Integer, nullable=False)
    reason = Column(Unicode(255), nullable=True)

    def accept_write_visitor(self, body):
        try:
            body.pop('balance')
        except KeyError:
            pass
        else:
            raise ForcedBalanceError("You cannot input the balance for a transaction")

        super(Transaction, self).accept_write_visitor(body)
        try:
            session.flush()
            last_transaction = Transaction.query.filter(Transaction.id != self.id).order_by('-id').first()
            old_balance = last_transaction.balance
        except AttributeError:
            old_balance = 0

        self.balance = old_balance + self.amount
        return self
