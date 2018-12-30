from helper.keycloak_helper import KeyCloakCrudHelper
from helper.notification_helper import NotificationCrudHelper


class UserCrudHelper(KeyCloakCrudHelper, NotificationCrudHelper):
    pass


class UserCrudHandler:
    def __init__(self, model_class):
        self.helper = UserCrudHelper(model_class)

    def create(self, body):
        return self.helper.create_helper(body)

    def read(self, model_uid):
        return self.helper.get_helper(model_uid)

    def update(self, model_uid, body):
        return self.helper.update_helper(model_uid, body)

    def bulk_update(self, body):
        return self.helper.bulk_update_helper(body)

    def search(self, filters):
        return self.helper.search_helper(filters)

    def delete(self, model_uid):
        return self.helper.delete_helper(model_uid)

    def notification(self, model_uid):
        return self.helper.get_notifications_helper(model_uid)
