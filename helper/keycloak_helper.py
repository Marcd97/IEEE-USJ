from flask import current_app, abort

from app_config.app_config import session
from configuration import KeyCloakMigrationError
from helper.simple_helper import CrudHelper


class KeyCloakCrudHelper(CrudHelper):

    @property
    def admin(self):
        policy_enforcer = current_app.extensions.get('policy_enforcer', None)
        return getattr(policy_enforcer.enforcer, 'admin_console', None)

    def create_helper(self, body):
        session.begin(nested=True)

        model_dict, _ = super(KeyCloakCrudHelper, self).create_helper(body)
        if current_app.config.get('KEYCLOAK_MIGRATION', False):
            model_instance = self.model_class.find(model_dict['uid'])
            try:
                model_instance.notify_keycloak_server(self.admin)
            except KeyCloakMigrationError as ex:
                session.rollback()
                abort(500, ex)

        session.commit()
        return model_dict, 201
