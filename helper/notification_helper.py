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
