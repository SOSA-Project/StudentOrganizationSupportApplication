import numpy as np
from app.backend.grade import Grade
from app.backend.subject import Subject

class GradeMonitor:
    def __init__(self, grades_list: np.ndarray):
        if not isinstance(grades_list, np.ndarray):
            raise TypeError("grades_list must be a NumPy array")

        self.grades_list = np.array(grades_list,dtype=str)

    def create_grade_table(self) -> []:
        grade_table = []
        for row in self.grades_list:
            grade_table.append(Grade(row[0],Subject(row[1],row[2])))
        return grade_table
