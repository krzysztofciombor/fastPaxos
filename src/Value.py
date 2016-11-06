class Value(object):
    def __init__(self, value: int, is_any: bool = False) -> None:
        self.value = value
        self.is_any = is_any


ANY = Value(-1, True)
