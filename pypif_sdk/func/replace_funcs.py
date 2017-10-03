import pypif
from pypif.util.case import to_camel_case
import json


def _recurse_replace(obj, key, new_key, sub, remove):
    """Recursive helper for `replace_by_key`"""
    if isinstance(obj, list):
        return [_recurse_replace(x, key, new_key, sub, remove) for x in obj]
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == key and v in sub:
                obj[new_key] = sub[v]
                if remove:
                    del obj[key]
            else:
                obj[k] = _recurse_replace(v, key, new_key, sub, remove)
    return obj


def replace_by_key(pif, key, subs, new_key=None, remove=False):
    """Replace values that match a key

    Deeply traverses the pif object, looking for `key` and
    replacing values in accordance with `subs`.  If `new_key`
    is set, the replaced values are assigned to that key.  If
    `remove` is `True`, the old `key` pairs are removed.
    """
    if not new_key:
        new_key = key
        remove = False
    orig = pif.as_dictionary()
    new  = _recurse_replace(orig, to_camel_case(key), to_camel_case(new_key), subs, remove)
    return pypif.pif.loads(json.dumps(new))
