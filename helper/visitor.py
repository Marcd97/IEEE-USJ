from configuration.exceptions import ModelFieldError


class ModelWriteVisitor:
    @staticmethod
    def visit_model(instance, body):
        for name in body:
            try:
                getattr(instance, name)
            except AttributeError:
                raise ModelFieldError("Field {} is not listed for this model".format(name))
            else:
                setattr(instance, name, body[name])
        return instance


class ModelReadVisitor:
    @staticmethod
    def visit_model(instance):
        instance_dict = instance.as_dict(instance.crud_metadata)
        return instance_dict
