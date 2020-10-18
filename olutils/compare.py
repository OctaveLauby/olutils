def content_diff(content1, content2):
    """Return differences b/w contents (list|set|...) in a dictionary

    About:
        Because 0 == False and 1 == True, diff may not work as wanted with
        list mixing booleans and integers.

    Return:
        (dict) with following items
            'common', set of common elements
            'minus', set of elements in list1 and not in list2
            'plus', set of elements in list2 and not in list1
    """
    set1 = set(content1)
    set2 = set(content2)
    common = set1.intersection(set2)
    return {
        'common': common,
        'minus': set1 - common,
        'plus': set2 - common,
    }
