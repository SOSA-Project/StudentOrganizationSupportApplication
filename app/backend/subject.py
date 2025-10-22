"""
File contains definition and implementation of Subject class
"""


class Subject:
    """
    Class stores information about a Subject
    """

    def __init__(self, name: str, ects_value: int) -> None:
        self.name = name
        self.ects_value = ects_value
