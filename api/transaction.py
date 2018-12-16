from flask import request, jsonify

from helper.simple_helper import SimpleCrudHandler
from models.transaction import Transaction

handler = SimpleCrudHandler(Transaction)


class TransactionApiExtension:
    def __init__(self, app):
        if app is not None:
            self.init_app(app)
        
    @staticmethod
    def init_app(app):
        app.add_url_rule('/transactions', 'create_transaction', create_transaction, methods=['POST'])
        app.add_url_rule('/transactions/<transaction_uid>', 'read_transaction', read_transaction, methods=['GET'])
        app.add_url_rule('/transactions/<transaction_uid>', 'update_transaction', update_transaction, methods=['PUT'])
        app.add_url_rule('/transactions/<transaction_uid>', 'delete_transaction', delete_transaction, methods=['DELETE'])
        app.add_url_rule('/transactions', 'search_transaction', search_transaction, methods=['GET'])
        app.add_url_rule('/transactions', 'bulk_update_transaction', bulk_update_transaction, methods=['PUT'])


def create_transaction():
    body = request.json
    jsonable_dict, code = handler.create(body)
    return jsonify(jsonable_dict), code


def read_transaction(transaction_uid):
    jsonable_dict, code = handler.read(transaction_uid)
    return jsonify(jsonable_dict), code


def update_transaction(transaction_uid):
    body = request.json
    jsonable_dict, code = handler.update(transaction_uid, body)
    return jsonify(jsonable_dict), code


def delete_transaction(transaction_uid):
    jsonable_dict, code = handler.delete(transaction_uid)
    return jsonify(jsonable_dict), code


def search_transaction():
    filters = dict(request.args)
    jsonable_dict, code = handler.search(filters)
    return jsonify(jsonable_dict), code


def bulk_update_transaction():
    body = request.json
    jsonable_dict, code = handler.bulk_update(body)
    return jsonify(jsonable_dict), code