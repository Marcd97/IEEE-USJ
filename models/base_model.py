__all__ = (
    'BaseModel',
)

from app_config.app_config import Base


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def create(cls):
        return cls()

    def as_dict(self, field_names):
        instance = dict()
        for field in field_names:
            instance[field] = getattr(self, field)
        return instance
