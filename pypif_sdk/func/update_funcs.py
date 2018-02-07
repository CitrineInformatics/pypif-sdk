from toolz import unique, concat
from pypif.pif import loads, dumps
import random


def _id(obj):
    """Get an id for deduping members"""
    return obj.get("name", random.random)


def _deep_update(old, new, extend):
    for k, v in new.items():
        if k not in old:
            old[k] = new[k]
        elif extend and isinstance(old[k], list) and isinstance(new[k], list):
            old[k] = list(unique(concat([new[k], old[k]]), _id))
        elif isinstance(old[k], dict) and isinstance(new[k], dict):
            _deep_update(old[k], new[k])
        else:
            old[k] = new[k]


def update(first, second, extend=False):
    old_d = first.as_dictionary()
    new_d = second.as_dictionary()
    _deep_update(old_d, new_d, extend)
    return loads(dumps(old_d))


def merge(first, second):
    return update(first, second, extend=True)
