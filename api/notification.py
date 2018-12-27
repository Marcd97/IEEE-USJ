from helper import as_dict

__all__ = (
    'NotificationApiExtension',
)

from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models import Notification

handler = SimpleCrudHandler(Notification)


class NotificationApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.add_url_rule('/notifications', 'create_notification', create_notification, methods=['POST'])
        app.add_url_rule('/notifications/<notification_uid>', 'read_notification', read_notification, methods=['GET'])
        app.add_url_rule('/notifications/<notification_uid>', 'update_notification', update_notification, methods=['PUT'])
        app.add_url_rule('/notifications/<notification_uid>', 'delete_notification', delete_notification, methods=['DELETE'])
        app.add_url_rule('/notifications', 'search_notification', search_notification, methods=['GET'])
        app.add_url_rule('/notifications', 'bulk_update_notification', bulk_update_notification, methods=['PUT'])


def create_notification():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_notification(notification_uid):
    jsonable_dict, code = handler.read(notification_uid)
    return jsonify(jsonable_dict), code


def update_notification(notification_uid):
    body = request.json
    jsonable_dict, code = handler.update(notification_uid, body)
    return jsonify(jsonable_dict), code


def delete_notification(notification_uid):
    jsonable_dict, code = handler.delete(notification_uid)
    return jsonify(jsonable_dict), code


def search_notification():
    filters = as_dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_notification():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code
