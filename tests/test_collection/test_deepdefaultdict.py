from olutils import dict2str
import olutils as lib


def readout(capfd):
    return capfd.readouterr()[0]


def test_defaultdict(capfd):

    dic = lib.defaultdict(int)
    dic['key_1'] += 1
    dic['key_3'] += 3

    string = dict2str(dic.to_dict())
    assert dic.pstring() == string
    dic.pprint()
    assert readout(capfd) == string + "\n"

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

    assert lib.deepdefaultdict(int, depth=0) == 0
    assert lib.deepdefaultdict(int, depth=-1) is None
    assert lib.deepdefaultdict(int, depth=-10) is None
