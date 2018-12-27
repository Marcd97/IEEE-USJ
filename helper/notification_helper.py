from helper.simple_helper import CrudHelper
from models import Notification


class NotificationCrudHelper(CrudHelper):
    def get_notifications_helper(self, uid_str):
        model_instance = self.model_class.find(uid_str)
        notifications = Notification.query.filter_by(target=model_instance, acknowledged=False).all()

        all_dicts = dict()
        for instance in notifications:
            result = self.read_visitor.visit_model(instance)
            all_dicts[result['uid']] = result
        return all_dicts, 200


class NotificationCrudHandler:
    def __init__(self, model_class):
        self.helper = NotificationCrudHelper(model_class)

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
