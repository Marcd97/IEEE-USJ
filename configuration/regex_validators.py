__all__ = (
    'PhoneValidator',
    'EmailValidator',
)

import re

from configuration import PhoneValidationError, EmailValidationError


class BaseValidator:
    regex = re.compile("")
    exception = Exception

    @classmethod
    def validate(cls, value):
        if not re.match(cls.regex, value):
            raise cls.exception()
        else:
            return value


class PhoneValidator(BaseValidator):
    """
    Validates the provided phone number against the following regex:
    +country_code prefix[ -/]8digit_number
    """

    regex = re.compile("^[+][0-9]{1,3}\s?[0-9]{1,2}[ -/]?[0-9]{6}$")
    exception = PhoneValidationError


class EmailValidator(BaseValidator):
    """
    Validates the provided email against the following regex:
    string@string.string
    where `string` does not contain the '@' sign
    """

    regex = re.compile("[^@]+@[^@]+\.[^@]+")
    exception = EmailValidationError
