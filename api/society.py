from app_config.app_config import policy_enforcer
from helper import as_dict

__all__ = (
    'SocietyApiExtension',
)

from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models.society import Society

handler = SimpleCrudHandler(Society)


class SocietyApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.add_url_rule('/societies', 'create_society', create_society, methods=['POST'])
        app.add_url_rule('/societies/<society_uid>', 'read_society', read_society, methods=['GET'])
        app.add_url_rule('/societies/<society_uid>', 'update_society', update_society, methods=['PUT'])
        app.add_url_rule('/societies/<society_uid>', 'delete_society', delete_society, methods=['DELETE'])
        app.add_url_rule('/societies', 'search_society', search_society, methods=['GET'])
        app.add_url_rule('/societies', 'bulk_update_society', bulk_update_society, methods=['PUT'])


@policy_enforcer.protected
def create_society():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


@policy_enforcer.protected
def read_society(society_uid):
    jsonable_dict, code = handler.read(society_uid)
    return jsonify(jsonable_dict), code


@policy_enforcer.protected
def update_society(society_uid):
    body = request.json
    jsonable_dict, code = handler.update(society_uid, body)
    return jsonify(jsonable_dict), code


@policy_enforcer.protected
def delete_society(society_uid):
    jsonable_dict, code = handler.delete(society_uid)
    return jsonify(jsonable_dict), code


@policy_enforcer.protected
def search_society():
    filters = as_dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


@policy_enforcer.protected
def bulk_update_society():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code
