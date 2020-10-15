"""Tools to build consistent plot decoration (labels, legends, fonts, ...)"""
import functools
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from olutils.params import read_params


# -------------------------------------------------------------------------- #
# Globals

DFT_FONT_PARAMS = {
    'title': {'size': 25, 'weight': "bold", 'family': "Perpetua"},
    'legend': {'size': 14},
    'xlabel': {'size': 16, 'weight': "semibold", 'family': "Verdana"},
    'ylabel': {'size': 16, 'weight': "semibold", 'family': "Verdana"},
    'xticks': {'size': 14},
    'yticks': {'size': 14},
}

DFT_PARAMS = {
    'xlabel': None,
    'ylabel': None,
    'title': None,
    'w_grid': True,
    'legend': {'loc': 'best'},
}

DECO_PARAMS_DOC_FRMT = (
    "\n{spaces}xlabel (str) : name of x-label"
    "\n{spaces}ylabel (str) : name of y-label"
    "\n{spaces}title (str)  : title of plot"
    "\n{spaces}w_grid (bool): display grid"
    "\n{spaces}legend (dict): parameters for legend"
    "\n{spaces}font_params (dict): parameters for fonts"
    "\n{spaces}    title, legend [xy]label, [xy]ticks (dict):"
    "\n{spaces}        @see matplotlib.font_manager.FontProperties"
    "\n{spaces}        family, style, variant, weight, stretch, size, fname"
)


def w_deco_params(n_spaces=12, beacon="<deco_param_descr>"):
    """Return decorator to add decoration params doc in function

    Args:
        n_spaces (int)  : number of spaces to add before each parameter in doc
        beacon (str)    : marker to replace with param description
    """
    assert isinstance(n_spaces, int)
    assert isinstance(beacon, str)

    def add_deco_params_doc(func):
        """Decorator for function with plot decoration parameters"""
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            """flat use of func"""
            return func(*args, **kwargs)
        func_wrapper.__doc__ = func.__doc__.replace(
            beacon, DECO_PARAMS_DOC_FRMT.format(spaces=" " * n_spaces)
        )
        return func_wrapper

    return add_deco_params_doc


# -------------------------------------------------------------------------- #
# Utils


@w_deco_params()
def decorate(subplot=None, **params):
    """Decorate graph using parameters

    Args:
        subplot (matplotlib.axes._subplots.AxesSubplot)
        **params: <deco_param_descr>
    """
    subplot = plt.gca() if subplot is None else subplot
    params, font_params = splitparams_(params)
    if params.xlabel:
        subplot.set_xlabel(params['xlabel'])
        subplot.xaxis.label.set_fontproperties(
            FontProperties(**font_params['xlabel'])
        )
    if params['ylabel']:
        subplot.set_ylabel(params['ylabel'])
        subplot.yaxis.label.set_fontproperties(
            FontProperties(**font_params['ylabel'])
        )
    if params['title']:
        plt.title(params['title'])
        subplot.title.set_fontproperties(
            FontProperties(**font_params['title'])
        )
    if params['w_grid']:
        plt.grid(True)

    for label in subplot.get_xticklabels():
        label.set_fontproperties(
            FontProperties(**font_params['xticks'])
        )
    for label in subplot.get_yticklabels():
        label.set_fontproperties(
            FontProperties(**font_params['yticks'])
        )

    if subplot.get_legend_handles_labels()[0]:
        prop = FontProperties(**font_params['legend'])
        subplot.legend(**params['legend'], prop=prop)


@w_deco_params()
def splitparams_(params, dft=None, fdft=None):
    """Extract font_params from params and return glb-params and font-params

    Args:
        params (dict)   : <deco_param_descr>
        dft (dict)      : @see DFT_PARAMS
        fdft (dict)     : @see DFT_FONT_PARAMS
    """
    font_params = params.pop("font_params", None)
    params = read_params(
        params, DFT_PARAMS if dft is None else dft, safe=False
    )
    font_params = read_params(
        font_params, DFT_FONT_PARAMS if fdft is None else fdft, safe=False
    )
    return params, font_params


# -------------------------------------------------------------------------- #
# PlotDesigner

class PlotDesigner:
    """Store plot-decorations when plotting same kind graph

    Example:
        >> params = {'xlabel': "time", 'ylabel': "pop", 'title': "pop evol"}
        >> designer = PlotDesigner(**params)
        >> years, pop = [2000, 2005, 2010, 2015], [59e6, 61e6, 63e6, 64e6]
        >> plt.plot(years, pop, label="France")
        >> designer.apply()
        >> plt.show()
    """

    @w_deco_params(n_spaces=16)
    def __init__(self, **params):
        """Initiate PlotDesigner

        Args:
            **params: <deco_param_descr>
        """
        self.params, self.font_params = splitparams_(params)

    @w_deco_params(n_spaces=16)
    def apply(self, subplot=None, **params):
        """Apply PlotDesigner to subplot

        Args:
            subplot (matplotlib.axes._subplots.AxesSubplot)
            **params: <deco_param_descr>
        """
        params, font_params = splitparams_(
            params, dft=self.params, fdft=self.font_params
        )
        decorate(subplot=subplot, font_params=font_params, **params)
