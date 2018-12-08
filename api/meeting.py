from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models.meeting import Meeting

handler = SimpleCrudHandler(Meeting)


class MeetingApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.add_url_rule('/path/meetings/', 'create_meeting', create_meeting, methods=['POST'])
        app.add_url_rule('/path/meetings/<meeting_uid>', 'read_meeting', read_meeting, methods=['GET'])
        app.add_url_rule('/path/meetings/<meeting_uid>', 'update_meeting', update_meeting, methods=['PUT'])
        app.add_url_rule('/path/meetings/<meeting_uid>', 'delete_meeting', delete_meeting, methods=['DELETE'])
        app.add_url_rule('/path/meetings/', 'search_meeting', search_meeting, methods=['GET'])
        app.add_url_rule('/path/meetings/', 'bulk_update_meeting', bulk_update_meeting, methods=['PUT'])


def create_meeting():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_meeting(meeting_uid):
    jsonable_dict, code = handler.read(meeting_uid)
    return jsonify(jsonable_dict), code


def update_meeting(meeting_uid):
    body = request.json
    jsonable_dict, code = handler.update(meeting_uid, body)
    return jsonify(jsonable_dict), code


def delete_meeting(meeting_uid):
    jsonable_dict, code = handler.delete(meeting_uid)
    return jsonify(jsonable_dict), code


def search_meeting():
    filters = dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_meeting():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code
