"""Comparison Tools"""

def content_diff(content1, content2, only_diff=False):
    """Return differences b/w contents (list|set|...) in a dictionary

    Args:
        content1 (iterable)
        content2 (iterable)
        only_diff (bool)    : also return common items

    About:
        Because 0 == False and 1 == True, diff may not work as wanted with
        list mixing booleans and integers.

    Return:
        (dict) with following items
            'minus', set of elements in content1 and not in content2
            'plus', set of elements in content2 and not in content1
            if not only_diff: 'common', set of common elements
    """
    set1 = set(content1)
    set2 = set(content2)
    common = set1.intersection(set2)
    res = {
        'minus': set1 - common,
        'plus': set2 - common,
    }
    if not only_diff:
        res['common'] = common
    return res
