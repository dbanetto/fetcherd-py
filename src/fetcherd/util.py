import re


def get_path(name, folders, default=None):
    for (k, v) in folders.items():
        if k == name.lower():
            return v
    return default


def get_path_regex(name, folders, default=None):
    for (k, v) in folders.items():
        if re.match(k, name.lower()):
            return v
    return default
