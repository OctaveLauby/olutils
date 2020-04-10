"""Tools to ease multi plotting"""
import matplotlib.pyplot as plt


class MultiPlotIterator:
    """Iterator for multi plot per line (convenient in notebooks)"""

    def __init__(self, n_cols=2, test_mode=False):
        """Init multi plot iterator

        Args:
            n_cols (int): number of plot per rows
            test_mode (bool): clear figure instead of showing it
        """
        self._count = 0
        self._n_cols = n_cols
        self._n_shows = 0

        if test_mode:
            self._show = plt.clf
        else:
            self._show = plt.show

    @property
    def count(self):
        """Current subplot number"""
        return self._count

    def increment(self):
        """Increment to next subplot (show if line is ended)"""
        if self.count and self.count % self.n_cols == 0:
            self.show()
        self._count += 1

    @property
    def n_cols(self):
        """Number of subplot per line"""
        return self._n_cols

    def endline(self):
        """End current line by showing it and set count back to 0"""
        if self.count:
            self.show()
        self._count = 0

    def next(self):
        """Go to next plot"""
        return next(self)

    def show(self):
        """Show figure"""
        self._n_shows += 1
        self._show()

    def __next__(self):
        self.increment()
        pos = self.count % self.n_cols
        pos = self.n_cols if pos == 0 else pos
        return plt.subplot(1, self.n_cols, pos)

    def __iter__(self):
        return self


def plotiter(elems, n_cols=2, w_subplot=False, **params):
    """Iter elems and create subplot for each element

    Show row-plots when row is completed or all elems are read

    Args:
        elems (iterable)    : element to iter upon
        n_cols (int)        : number of plot per row
        w_subplot (bool)    : also yield subplot
            (matplotlib.axes._subplots.AxesSubplot)
        **params: @see MultiPlotIterator

    Return:
        (iterable)
            if w_subplot: yield (subplot, elem)
            else: yield elem
    """
    plotiterator = MultiPlotIterator(n_cols, **params)
    for elem in elems:
        subplot = plotiterator.next()

        if w_subplot:
            yield subplot, elem
        else:
            yield elem
    plotiterator.endline()
