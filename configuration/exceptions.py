__all__ = (
    'ModelFieldError',
    'UIDValueError',
)


class ModelFieldError(Exception):
    pass

class UIDValueError(ValueError):
    pass
