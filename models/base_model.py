__all__ = (
    'BaseModel',
)

from app_config.app_config import Base
from configuration import ModelFieldError


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def create(cls):
        return cls()

    def accept_read_visitor(self, field_names):
        instance = dict()
        for field in field_names:
            instance[field] = getattr(self, field)
        return instance

    def accept_write_visitor(self, body):
        for name in body:
            try:
                getattr(self, name)
            except AttributeError:
                raise ModelFieldError("Field {} is not listed for this model".format(name))
            else:
                setattr(self, name, body[name])
        return self
