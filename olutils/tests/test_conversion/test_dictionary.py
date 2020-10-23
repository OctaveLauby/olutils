from collections import OrderedDict

import olutils as lib


def test_basedict():

    dic = OrderedDict([
        ('sub_odict', OrderedDict([('key_1', 1), ('key_2', 2)])),
        ('key', "value"),
        ('odict_l', [
                OrderedDict([('k', 3)]),
                OrderedDict([('k', 4)]),
        ])
    ])

    dic = lib.basedict(dic)
    assert type(dic) == dict
    assert type(dic['sub_odict']) == dict
    assert type(dic['odict_l'][0]) == OrderedDict
    assert type(dic['odict_l'][1]) == OrderedDict
    assert dic == {
        'sub_odict': {'key_1': 1, 'key_2': 2},
        'key': "value",
        'odict_l': [{'k': 3}, {'k': 4}]
    }


def test_dict2str():
    obj = OrderedDict([
        ('1', 11),
        ('two', 22),
        (12345, {'trente': 333, '32': {}}),
        ('4', {'5': OrderedDict([
            ('a', "salut"),
            ('b', "hello"),
            ('cde', [1, 2]),
        ])}),
    ])
    assert lib.dict2str(obj) == (
        "# 1    : 11"
        "\n# two  : 22"
        "\n# 12345:"
        "\n\t* trente: 333"
        "\n\t* 32    : <empty dict>"
        "\n# 4    :"
        "\n\t* 5:"
        "\n\t\t> a  : salut"
        "\n\t\t> b  : hello"
        "\n\t\t> cde: [1, 2]"
    )
    assert lib.dict2str(
        obj, bullets="*-", indent="  ", prefix="|", leafconv=repr, keyconv=repr
    ) == (
        "|* '1'  : 11"
        "\n|* 'two': 22"
        "\n|* 12345:"
        "\n|  - 'trente': 333"
        "\n|  - '32'    : <empty dict>"
        "\n|* '4'  :"
        "\n|  - '5':"
        "\n|    'a'  : 'salut'"
        "\n|    'b'  : 'hello'"
        "\n|    'cde': [1, 2]"
    )
    assert lib.dict2str({}) == "<empty dict>"
    assert lib.dict2str("hello", leafconv=repr) == "'hello'"
