"""Functions for convenient plotting (mostly for notebooks)"""

import matplotlib.pyplot as plt

from .decoration import (
    decorate,
    DFT_FONT_PARAMS,
    DFT_PARAMS,
    PlotDesigner,
)
from .multiplot import (
    MultiPlotIterator,
    plotiter,
)


# plt.style.use('seaborn-deep')


def resize(width=17, height=4):
    """Pretty doll function to reshape plot box in notebook"""
    plt.rcParams['figure.figsize'] = [width, height]
