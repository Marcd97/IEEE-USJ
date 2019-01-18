from flask import abort

from app_config.app_config import session
from configuration.exceptions import ModelFieldError
from helper.visitor import ModelWriteVisitor, ModelReadVisitor


class CrudHelper:
    def __init__(self, model_class, write_visitor=ModelWriteVisitor, read_visitor=ModelReadVisitor):
        self.model_class = model_class
        self.write_visitor = write_visitor()
        self.read_visitor = read_visitor()

    def create_helper(self, body):
        model_instance = self.model_class.create()
        session.add(model_instance)
        try:
            model_instance = self.write_visitor.visit(model_instance, body)
        except ModelFieldError as ex:
            abort(400, ex)
        else:
            session.flush()
            session.commit()
            model_dict = self.read_visitor.visit_model(model_instance)
            return model_dict, 201

    def get_helper(self, uid_str):
        model_instance = self.model_class.find(uid_str)
        model_dict = self.read_visitor.visit_model(model_instance)
        return model_dict, 200

    def update_helper(self, uid_str, body):
        model_instance = self._update(uid_str, body)
        session.commit()

        jsonable_dict = self.read_visitor.visit_model(model_instance)
        return jsonable_dict, 200

    def bulk_update_helper(self, body):
        total_changes = 0
        for uid_str, value in body.items():
            self._update(uid_str, value)
            total_changes += 1

        session.commit()
        return dict(changes=total_changes), 200

    def _update(self, uid_str, body):
        model_instance = self.model_class.find(uid_str)

        model_instance = self.write_visitor.visit(model_instance, body)
        session.flush()
        return model_instance

    def search_helper(self, filters):
        query = self.model_class.query
        query = query.filter_by(**filters)

        all_results = query.all()
        all_dicts = dict()
        for instance in all_results:
            result = self.read_visitor.visit_model(instance)
            all_dicts[result['uid']] = result
        return all_dicts, 200

    def delete_helper(self, uid_str):
        try:
            model_instance = self.model_class.find(uid_str)
        except Exception as ex:
            abort(500, ex)
        else:
            session.delete(model_instance)
            session.flush()
            session.commit()
            return None, 204


class SimpleCrudHandler:
    def __init__(self, model_class):
        self.helper = CrudHelper(model_class)

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
