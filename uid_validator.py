import re
from collections import namedtuple
from hashids import Hashids

from configuration.enums import StrEnums
from configuration.exceptions import UIDValueError

Uid = namedtuple('Uid', 'prefix,serial_id')


class Prefix(StrEnums):
    ANY = 'ANY'
    VALID = 'VALID'


class UIDValidator:
    VALID_PREFIXES = dict(
        DFT=0x00,  # Default
        MBR=0x5A,  # Member
        USR=0x71,  # User
        TRS=0xE3,  # Transaction
        EVT=0xF1,  # Event
        MTG=0x17,  # Meeting
        SCT=0x9E,  # Society
    )

    UID_REGEX = re.compile('^([A-Z]{3})_([a-zA-Z0-9]+)?$')  # Regular expression defining the UID

    VERIFIER = 0xAE  # Random number just to make sure that the decoding works properly

    def __init__(self, prefix=Prefix.VALID):
        self.prefix = prefix
        self.hashids = Hashids()

    def decode(self, value):
        """
        Decodes a Regex of type XXX_abcdef into a UID of type (Prefix, Serial_ID)

        :param str. value: Hashed ID to decode
        :rtype: (str, int)
        """

        match = self.UID_REGEX.match(value)
        if not match:
            raise UIDValueError('Value is not a Regular Expression')

        prefix, hashed_id = match.groups()

        if self.prefix == Prefix.ANY:
            pass
        else:
            if prefix not in self.VALID_PREFIXES:
                raise UIDValueError('Invalid prefix')

        try:
            prefix_id, serial_id, verifier = self.hashids.decode(hashed_id)
        except ValueError as ex:
            raise UIDValueError('The prefix or verifier is missing') from ex
        else:
            expected_prefix_id = self.VALID_PREFIXES.get(prefix, 0x00)
            if prefix_id != expected_prefix_id or verifier != self.VERIFIER:
                raise UIDValueError('The prefix or verifier are incorrect')

        return Uid(prefix=prefix, serial_id=serial_id)

    def encode(self, uid, valid=True):
        """
        Encodes a UID of type (Prefix, Serial_ID) into a regex of type XXX_abcdef

        :param Uid uid: UID to be hashed
        :param bool valid: Allows to bypass the Validity Check if set to False

        :rtype: str
        :return: Hashed ID
        """
        if uid is None:
            return
        if uid.serial_id is None:
            return
        if valid and uid.prefix not in self.VALID_PREFIXES:
            raise UIDValueError('Invalid prefix {!r}'.format(uid.prefix))

        prefix = self.VALID_PREFIXES.get(uid.prefix, 0x00)
        hashed_id = self.hashids.encode(prefix, uid.serial_id, self.VERIFIER)

        if hashed_id == '':
            raise UIDValueError('Invalid serial id {!r}'.format(uid.serial_id))

        return '{prefix}_{hashed_id}'.format(prefix=uid.prefix, hashed_id=hashed_id)


def parse_uid(value):
    """
    Parses a hashed ID and returns the Serial ID

    :param str value: Hashed ID
    :rtype: Uid
    """
    validator = UIDValidator()
    serial_id = validator.decode(value)
    return serial_id


def uid_str(**uid):
    """
    Hashed an ID of type (Prefix, Serial_ID)

    :param uid: ID to hash
    :rtype: str
    """
    validator = UIDValidator()
    return validator.encode(Uid(**uid))
