from matplotlib.axes._subplots import SubplotBase

from olutils import plotting


# /!\\ Not testing much here, but at least test if its running


def test_MultiPlotIterator():
    plotiter = plotting.MultiPlotIterator(n_cols=3, test_mode=True)
    assert plotiter.count == 0
    assert plotiter.n_cols == 3
    assert plotiter._n_shows == 0

    subplot = plotiter.next()
    assert isinstance(subplot, SubplotBase)
    assert plotiter.count == 1

    assert plotiter.next() != subplot
    plotiter.next()
    assert plotiter._n_shows == 0

    plotiter.next()
    assert plotiter.count == 4
    assert plotiter._n_shows == 1

    plotiter.endline()
    assert plotiter._n_shows == 2
    assert plotiter.count == 0
    assert plotiter.n_cols == 3


def test_plotiter():
    count = 0
    prev_subplot = None
    plot_iterator = plotting.plotiter(
        [1, 2, 3], w_subplot=True, n_cols=2, test_mode=True
    )
    for subplot, element in plot_iterator:
        count += 1
        assert count == element
        assert subplot != prev_subplot
        assert isinstance(subplot, SubplotBase)
        prev_subplot = subplot
