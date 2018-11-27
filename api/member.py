from helper import as_dict

__all__ = (
    'MemberApiExtension',
)

from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models.member import Member

handler = SimpleCrudHandler(Member)


class MemberApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.add_url_rule('/members', 'create_member', create_member, methods=['POST'])
        app.add_url_rule('/members/<member_uid>', 'read_member', read_member, methods=['GET'])
        app.add_url_rule('/members/<member_uid>', 'update_member', update_member, methods=['PUT'])
        app.add_url_rule('/members/<member_uid>', 'delete_member', delete_member, methods=['DELETE'])
        app.add_url_rule('/members', 'search_member', search_member, methods=['GET'])
        app.add_url_rule('/members', 'bulk_update_member', bulk_update_member, methods=['PUT'])


def create_member():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_member(member_uid):
    jsonable_dict, code = handler.read(member_uid)
    return jsonify(jsonable_dict), code


def update_member(member_uid):
    body = request.json
    jsonable_dict, code = handler.update(member_uid, body)
    return jsonify(jsonable_dict), code


def delete_member(member_uid):
    jsonable_dict, code = handler.delete(member_uid)
    return jsonify(jsonable_dict), code


def search_member():
    filters = as_dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_member():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code