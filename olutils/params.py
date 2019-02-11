"""Utils to manage parameters and arguments"""
import itertools


class Param(dict):

    def __getattr__(self, attr):
        """Return stat associated to attr if attr is not an attribute.

        About
        -----
            Stats related to x can be gather as day by adding #d in attr
            For instance : stats.#d
        """
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(
                "%s is neither a param attribute nor a field" % attr
            ) from None

    def __setattr__(self, attr, val):
        if attr in self:
            self[attr] = val
        else:
            raise AttributeError(
                "%s is neither a param attribute nor a field" % attr
            )


def check_type(name, value, exp_type):
    """Simple check of param type, raising TypeError with explicit message

    Args:
        name (str)      : parameter name to display in error message
        value (object)  : parameter value to check the type of
        exp_type (type or tuple): expected type of parameter

    Raise:
        (TypeError) if type not correct
    """
    if not isinstance(value, exp_type):
        raise TypeError(
            "parameter %s should be %s instance, got %s: %s"
            % (name, exp_type, type(value), repr(value))
        )


def read_params(params, dft_params, safe=True):
    """Return params completed with dft params in convenient dict-like object

    Args:
        params (NoneType or dict): list of params given by user
        dft_params (dict): expected parameters with default values
        safe (bool): raises KeyError if params contains key not in dft_params

    Return:
        (Param) dict-like structure where params are accessible as attributes
    """
    params = {} if params is None else params
    assert isinstance(params, dict) and isinstance(dft_params, dict), (
        "read_params expect dict arguments : got %s and %s"
        % (type(params), type(dft_params))
    )
    res = dft_params.copy()
    wrong_params = []
    params = params if params else {}
    for key, val in params.items():
        if key not in res:
            wrong_params.append(key)
        res[key] = val
    if wrong_params and safe:
        raise KeyError("Unexpected params : %s" % ", ".join(wrong_params))
    return Param(res)


def iter_params(param_ranges):
    """Return iterator on all possible param value associations

    Args:
        param_ranges (dict of list): for each parameter, possible values

    Example:
        >> param_iter = iter_params({'int': [1, 2], 'str': ["a", "b"]})
        >> next(param_iter)
        {'int': 1, 'str': 'a'}
        >> for string in param_iter: print(string)
        {'int': 1, 'str': 'b'}
        {'int': 2, 'str': 'a'}
        {'int': 2, 'str': 'b'}
        >> next(param_iter)
        StopIteration

    Return:
        (iterator)
    """
    params, ranges = [], []
    for param, prange in param_ranges.items():
        params.append(param)
        ranges.append(prange)

    def params_iter(params, ranges):
        for param_set in itertools.product(*ranges):
            yield {
                param: value
                for param, value in zip(params, param_set)
            }
    return params_iter(params, ranges)


def add_dft_args(parser, dft_args, flag_prefix="", help_prefix=""):
    """Add arguments to parser.

    Args:
        parser (argparse.ArgumentParser): parser you want to complete
        dft_args    (dict): default arguments (arg_name, dft_value)
        flag_prefix (str):  prefix before flag
        help_prefix (str):  prefix before help
    """
    for param, dft_value in dft_args.items():
        param_flag = "--%s%s" % (flag_prefix, param)
        if isinstance(dft_value, bool):
            action = "store_false" if dft_value else "store_true"
            parser.add_argument(
                param_flag, action=action,
                help="%s%s" % (help_prefix, param)
            )
        else:
            parser.add_argument(
                param_flag, required=False, default=dft_value,
                help="%s%s, default is %s" % (help_prefix, param, dft_value)
            )
