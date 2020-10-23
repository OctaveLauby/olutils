import olutils as lib


def test_defaultdict():

    dic = lib.defaultdict(int)
    dic['key_1'] += 1
    dic['key_3'] += 3
    dic = dic.to_dict()
    assert type(dic) == dict
    assert dic == {'key_1': 1, 'key_3': 3}


def test_deepdefaultdict():

    dic = lib.deepdefaultdict(int, depth=2)
    dic['key_1']['key_1'] += 11
    dic['key_1']['key_2'] += 12
    dic['key_2']['key_1'] += 21
    dic = dic.to_dict()
    assert type(dic) == dict
    assert type(dic['key_1']) == dict
    assert type(dic['key_2']) == dict
    assert dic == {'key_1': {'key_1': 11, 'key_2': 12}, 'key_2': {'key_1': 21}}
