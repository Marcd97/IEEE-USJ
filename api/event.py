from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models.event import Event

handler = SimpleCrudHandler(Event)


class EventApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)
        
    @staticmethod
    def init_app(app):
        app.add_url_rule('/events', 'create_event', create_event, methods=['POST'])
        app.add_url_rule('/events/<event_uid>', 'read_event', read_event, methods=['GET'])
        app.add_url_rule('/events/<event_uid>', 'update_event', update_event, methods=['PUT'])
        app.add_url_rule('/events/<event_uid>', 'delete_event', delete_event, methods=['DELETE'])
        app.add_url_rule('/events', 'search_event', search_event, methods=['GET'])
        app.add_url_rule('/events', 'bulk_update_event', bulk_update_event, methods=['PUT'])


def create_event():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_event(event_uid):
    jsonable_dict, code = handler.read(event_uid)
    return jsonify(jsonable_dict), code


def update_event(event_uid):
    body = request.json
    jsonable_dict, code = handler.update(event_uid, body)
    return jsonify(jsonable_dict), code


def delete_event(event_uid):
    jsonable_dict, code = handler.delete(event_uid)
    return jsonify(jsonable_dict), code


def search_event():
    filters = dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_event():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code