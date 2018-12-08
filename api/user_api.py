from flask import request, jsonify

from helper import as_dict
from helper.simple_helper import SimpleCrudHandler
from models.user import User

handler = SimpleCrudHandler(User)


class UserApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.add_url_rule('/users', 'create_user', create_user, methods=['POST'])
        app.add_url_rule('/users/<user_uid>', 'read_user', read_user, methods=['GET'])
        app.add_url_rule('/users/<user_uid>', 'update_user', update_user, methods=['PUT'])
        app.add_url_rule('/users/<user_uid>', 'delete_user', delete_user, methods=['DELETE'])
        app.add_url_rule('/users', 'search_user', search_user, methods=['GET'])
        app.add_url_rule('/users', 'bulk_update_user', bulk_update_user, methods=['PUT'])


def create_user():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_user(user_uid):
    jsonable_dict, code = handler.read(user_uid)
    return jsonify(jsonable_dict), code


def update_user(user_uid):
    body = request.json
    jsonable_dict, code = handler.update(user_uid, body)
    return jsonify(jsonable_dict), code


def delete_user(user_uid):
    jsonable_dict, code = handler.delete(user_uid)
    return jsonify(jsonable_dict), code


def search_user():
    filters = as_dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_user():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code