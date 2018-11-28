__all__ = (
    'UIDValueError',
    'ModelFieldError',
    'ModelValidationError',
)


class UIDValueError(ValueError):
    pass


class ModelFieldError(Exception):
    pass


class ModelValidationError(Exception):
    pass
