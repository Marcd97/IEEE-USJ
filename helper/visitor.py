class ModelWriteVisitor:
    @staticmethod
    def visit(instance, body):
        return instance.accept_write_visitor(body)


class ModelReadVisitor:
    @staticmethod
    def visit_model(instance):
        return instance.accept_read_visitor(instance.crud_metadata)
