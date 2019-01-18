__all__ = (
    'UIDValueError',
    'ModelFieldError',
    'ModelValidationError',
    'EmailValidationError',
    'PhoneValidationError',
    'ForcedBalanceError',
    'KeyCloakMigrationError'
)


class UIDValueError(ValueError):
    pass


class ModelFieldError(Exception):
    pass


class ModelValidationError(Exception):
    pass


class EmailValidationError(Exception):
    pass


class PhoneValidationError(Exception):
    pass


class ForcedBalanceError(Exception):
    pass


class KeyCloakMigrationError(Exception):
    pass
