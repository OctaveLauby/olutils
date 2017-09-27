"""Utils to manage parameters and arguments"""


def read_params(params, dft_params):
    """Return parameters completed with default.

    Args:
        params      (dict): user parameters
        dft_params  (dict): dft parameters

    Returns:
        (dict): user parameters completed with defaults

    Raises:
        KeyError when user parameters are not all in dft parameters
    """
    res_params = dict(dft_params)

    unknown_keys = []
    for (key, value) in params.items():
        if key not in res_params:
            unknown_keys.append(key)
        elif value is not None:
            res_params[key] = value

    if unknown_keys:
        raise KeyError(
            "Unexpected keys in params: %s" % ", ".join(map(str, unknown_keys))
        )

    return res_params


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
