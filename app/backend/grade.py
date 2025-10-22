"""
File contains definition and implementation of Grade class
"""

from app.backend.subject import Subject


class Grade:
    """
    Class stores information about a Grade
    """

    def __init__(self, value: float, subject: Subject, weight: float = 1) -> None:
        self.value = value
        self.subject = subject
        self.weight = weight
