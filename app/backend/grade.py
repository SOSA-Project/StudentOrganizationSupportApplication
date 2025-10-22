from app.backend.subject import Subject

class Grade:
    def __init__(self, value: float, subject: Subject):
        self.value = value
        self.subject = subject