class SpeStr(str):
    """String where representation has no ' around"""
    def __repr__(self):
        return str(self)
