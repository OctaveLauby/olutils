import olutils.collection.singleton as lib


def test_singleton():

    class Class1(metaclass=lib.Singleton):
        def __init__(self, value):
            self.value = value

    class Class2(Class1):
        def __init__(self, value, name):
            super().__init__(value)
            self.name = name

    instance_1 = Class1(8)
    instance_1_redefined = Class1(9)

    assert instance_1 is instance_1_redefined
    assert instance_1.value == 8

    instance_2 = Class2(30, "stephen")
    instance_2_redefined = Class2(3, "allen")

    assert instance_2 is instance_2_redefined
    assert instance_2 is not instance_1
    assert instance_2.value == 30
    assert instance_2.name == "stephen"
