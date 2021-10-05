"""Flat string (not single quote in repr)"""


class FlatStr(str):
    """String with no ' around repr"""

    def __repr__(self) -> str:
        return str(self)
