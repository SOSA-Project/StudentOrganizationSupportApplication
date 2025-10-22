class Subject:
    def __init__(self, name: str, ects_value: int):
        self.name = name
        self.ects_value = ects_value

    def __eq__(self, other):
        if isinstance(other, Subject):
            return self.name == other.name
        return False
