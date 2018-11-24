__all__ = (
    'UIDValueError',
    'ModelFieldError',
)


class UIDValueError(ValueError):
    pass


class ModelFieldError(Exception):
    pass
