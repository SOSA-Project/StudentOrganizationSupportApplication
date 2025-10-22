from app.backend.subject import Subject


class Grade:
    def __init__(self, value: float, subject: Subject, weight: float = 1):
        self.value = value
        self.subject = subject
        self.weight = weight
