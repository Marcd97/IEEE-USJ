from .visitor import *


def as_dict(filters):
    filters_dict = dict(filters)
    for key, value in filters_dict.items():
        assert isinstance(value, list)
        assert len(value) == 1
        value = value[0]
        filters_dict[key] = value
    return filters_dict
