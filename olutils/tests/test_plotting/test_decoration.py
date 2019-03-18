import matplotlib.pyplot as plt
import pytest

from olutils import plotting

# /!\\ Test could be highly improved


YEARS, POP = [2000, 2005, 2010, 2015], [59e6, 61e6, 63e6, 64e6]
XLABEL, YLABEL, TITLE = "time", "pop", "pop_evol"


def myfunc(**params):
    """This is my docstring

    Args:
        **params: <beacon>

    Return:
        (NoneType)
    """
    return


def assert_fontequal(properties, expected_properties):
    for key, value in expected_properties.items():
        value = [value] if key == "family" else value
        assert getattr(properties, "_" + key) == value


def assert_dftfonts(subplot, skip=[]):

    if 'legend' not in skip:
        legend = subplot.legend_
        assert_fontequal(legend.prop, plotting.DFT_FONT_PARAMS['legend'])

    if 'title' not in skip:
        properties = subplot.title.get_fontproperties()
        assert_fontequal(properties, plotting.DFT_FONT_PARAMS['title'])

    if 'xlabel' not in skip:
        properties = subplot.xaxis.label.get_fontproperties()
        assert_fontequal(properties, plotting.DFT_FONT_PARAMS['xlabel'])

    if 'ylabel' not in skip:
        properties = subplot.yaxis.label.get_fontproperties()
        assert_fontequal(properties, plotting.DFT_FONT_PARAMS['ylabel'])

    if 'xticks' not in skip:
        xtick_labels = subplot.get_xticklabels()
        for label in xtick_labels:
            properties = label.get_fontproperties()
            assert_fontequal(properties, plotting.DFT_FONT_PARAMS['xticks'])

    if 'yticks' not in skip:
        ytick_labels = subplot.get_yticklabels()
        for label in ytick_labels:
            properties = label.get_fontproperties()
            assert_fontequal(properties, plotting.DFT_FONT_PARAMS['yticks'])


def test_w_deco_params():

    w_deco_params = plotting.decoration.w_deco_params

    with pytest.raises(AssertionError):
        w_deco_params(myfunc)

    nfunc = w_deco_params(beacon="<beacon>")(myfunc)
    assert "xlabel" in nfunc.__doc__
    assert "ylabel" in nfunc.__doc__
    assert "title" in nfunc.__doc__
    assert "w_grid" in nfunc.__doc__
    assert "legend" in nfunc.__doc__
    assert "font_params" in nfunc.__doc__


def test_decorate():

    subplot = plt.subplot(1, 1, 1)
    plt.plot(YEARS, POP, label="France")

    assert subplot._axes_locator is None
    assert subplot.legend_ is None
    assert subplot.title._text == ""
    assert subplot.xaxis.label._text == ""
    assert subplot.yaxis.label._text == ""

    # Decorate with default

    plotting.decorate(title=TITLE, xlabel=XLABEL, ylabel=YLABEL)

    legend = subplot.legend_
    assert len(legend.texts) == 1
    assert legend.texts[0]._text == "France"
    assert subplot.title._text == TITLE
    assert subplot.xaxis.label._text == XLABEL
    assert subplot.yaxis.label._text == YLABEL
    assert_dftfonts(subplot)

    # Decorate with personalized
    # # TODO : implement the tests
    # # plt.clf(); subplot = plt.subplot(1, 1, 1); ...


def test_splitparams_():

    splitparams_ = plotting.decoration.splitparams_

    params_all = {
        'xlabel': XLABEL,
        'title': TITLE,
        'font_params': {
            'title': {'size': 17}
        }
    }
    params, font_params = splitparams_(params_all)
    assert params == {
        param: (
            XLABEL
            if param == 'xlabel'
            else (
                TITLE
                if param == 'title'
                else value
            )
        )
        for param, value in plotting.DFT_PARAMS.items()
    }
    assert font_params == {
        param: (
            {'size': 17}
            if param == 'title'
            else value
        )
        for param, value in plotting.DFT_FONT_PARAMS.items()
    }

    params_all2 = {
        'font_params': {'xticks': {'family': "Verdana"}}
    }
    params2, font_params2 = splitparams_(
        params_all2, dft=params, fdft=font_params
    )
    assert params2 == params
    assert font_params2 == {
        param: (
            {'family': "Verdana"}
            if param == 'xticks'
            else value
        )
        for param, value in font_params.items()
    }


def test_PlotDesigner():

    params = {'xlabel': XLABEL, 'ylabel': YLABEL, 'title': TITLE}
    designer = plotting.PlotDesigner(**params)
    years, pop = [2000, 2005, 2010, 2015], [59e6, 61e6, 63e6, 64e6]

    plt.plot(years, pop, label="France")
    designer.apply()
    subplot = plt.gca()
    assert subplot.title._text == TITLE
    assert subplot.xaxis.label._text == XLABEL
    assert subplot.yaxis.label._text == YLABEL
    assert_dftfonts(subplot)
    plt.clf()

    plt.plot(years, pop, label="France")
    designer.apply(font_params={'title': {'size': 17}})
    subplot = plt.gca()
    assert subplot.title._text == TITLE
    assert subplot.xaxis.label._text == XLABEL
    assert subplot.yaxis.label._text == YLABEL
    assert_dftfonts(subplot, skip="title")
    assert_fontequal(subplot.title.get_fontproperties(), {'size': 17})
    plt.clf()
