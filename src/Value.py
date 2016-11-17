class Value(object):
    def __init__(self, value: int, is_any: bool = False) -> None:
        self.value = value
        self.is_any = is_any

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == other.value and self.is_any == other.is_any


ANY = Value(-1, True)
