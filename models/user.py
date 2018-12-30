__all__ = (
    'User',
)

from sqlalchemy import Column, Unicode
from sqlalchemy.orm import validates

from configuration import EmailValidator, PhoneValidator, KeyCloakMigrationError
from .base_model import BaseModel
from .base_uid import UidModel, IdModel


class User(UidModel, IdModel, BaseModel):
    __tablename__ = 'users'
    UID_PREFIX = 'USR'

    crud_metadata = ['email', 'username', 'phone_number', 'first_name', 'last_name', 'uid', 'role']

    email = Column(Unicode(255), nullable=True)
    username = Column(Unicode(255), nullable=False)
    phone_number = Column(Unicode(255), nullable=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    role = Column(Unicode(255), nullable=False)

    def notify_keycloak_server(self, admin):
        user_payload = dict(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        try:
            user_id = admin.create_user(user_payload)
            role = admin.get_realm_role(self.role)
            admin.assign_user_realm_role(user_id, role)
        except Exception:
            raise KeyCloakMigrationError()

    @validates('email')
    def validate_email(self, key, email):
        return EmailValidator.validate(email)

    @validates('phone_number')
    def validate_phone(self, key, phone):
        return PhoneValidator.validate(phone)
