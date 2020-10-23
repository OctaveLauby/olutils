"""Special strings3"""

class SpeStr(str):
    """String with no ' around repr"""
    def __repr__(self):
        return str(self)
