"""Utils to manage common python objects."""
import json
import os
import pickle


def load(path, method=None):
    """Load obj at path given a method (json or pickle).

    method=None to catch method from path extension.
    """
    if method is None:
        method = path.split(".")[-1]

    res = None
    if method == "json":
        with open(path) as file:
            res = json.load(file)
    elif method == "pickle":
        with open(path, "rb") as file:
            res = pickle.load(file)
    else:
        raise ValueError("Unknown method %s" % method)
    return res


def save(obj, path, method=None):
    """Save obj to path given a method (json or pickle).

    method=None to catch method from path extension.
    """
    directory = os.path.dirname(path)

    if method is None:
        method = path.split(".")[-1]

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if method == "json":
        with open(path, "w") as file:
            json.dump(
                obj, file, sort_keys=True, indent=4, separators=(',', ': ')
            )
    elif method == "pickle":
        with open(path, "wb") as file:
            pickle.dump(obj, file)
    else:
        raise ValueError("Unknown method %s" % method)
