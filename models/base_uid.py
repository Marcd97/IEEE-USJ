__all__ = (
    'UidModel',
    'IdModel',
)

from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declared_attr

from configuration.exceptions import ModelValidationError
from uid_validator import uid_str, parse_uid, Uid


def id_with_sequence():
    class IdWithSequence(object):
        @declared_attr.cascading
        def id(self):
            col_type = Integer
            col_kwargs = dict(autoincrement=True)
            info = dict(
                generated=True,
                ordering=0,
                exposed_name='id',
                type='Integer',
                nullable=False,
                unique=True,
            )
            col_args = getattr(self, '__id_args__', tuple())
            col_kwargs.update(getattr(self, '__id_kwargs__', dict()))
            id = Column(col_type, *col_args, primary_key=True, info=info, **col_kwargs)
            id._creation_order = -1
            return id
    return IdWithSequence


class UidModel:
    """
    Class that serves as base for all the Models with a UID.
    For any class that inherits this one, UID_PREFIX should be overwritten by the correct value
    """

    UID_PREFIX = "XXX"

    @property
    def uid(self):
        return uid_str(prefix=self.UID_PREFIX, serial_id=self.id)

    @uid.setter
    def uid(self, value):
        uid = parse_uid(value)
        if uid.prefix != self.UID_PREFIX:
            raise ModelValidationError("Invalid UID {!r}; expected prefix {!r}".format(value, self.UID_PREFIX))
        self.id = uid.serial_id

    @classmethod
    def find(cls, identifier):
        """
        Gets the SQLAlchemy instance that matches the identifier.

        :param identifier: Uid or hashed Uid
        :return: Model Instance
        """

        if isinstance(identifier, Uid):
            uid = identifier
        else:
            uid = parse_uid(identifier)
        if uid.prefix != cls.UID_PREFIX:
            raise ModelValidationError("Invalid UID {!r}; expected prefix {!r}".format(identifier, cls.UID_PREFIX))
        pkey_value = uid.serial_id if uid is not None else None
        if pkey_value is None:
            return None
        return cls.query.get_or_404(pkey_value)


class IdModel(id_with_sequence()):
    pass
