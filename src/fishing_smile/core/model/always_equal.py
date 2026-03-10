class AlwaysEqual[T]:
    """Used for excluding pydantic private attribute from being used in equality checks"""
    def __init__(self, value: T):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, AlwaysEqual):
            return NotImplemented
        return True

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'

