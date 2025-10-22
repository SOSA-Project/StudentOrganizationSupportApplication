"""
File contains definition for GradeMonitor class and its functionality
"""

import numpy as np
from app.backend.grade import Grade
from app.backend.subject import Subject


class GradeMonitor:
    """
    Purpose of the class is to collect, manage and operate of grade data from the database.
    """

    def __init__(self, grades_list: np.ndarray) -> None:
        self.grade_table: list[Grade] = []
        self.subject_table: list[Subject] = []
        self.fill_monitor_tables(grades_list)

    def fill_monitor_tables(self, grades_list: np.ndarray) -> None:
        """
        Method fills monitor's tables with data fetched from database.
        :param grades_list: table of grades data fetched from database
        :return: nothing
        """
        for row in grades_list:
            if len(self.subject_table) == 0:
                current_subject = Subject(row[1], int(row[2]))
                self.subject_table.append(current_subject)
            else:
                subject_in_table = False
                for subject in self.subject_table:
                    if subject.name == row[1]:
                        current_subject = subject
                        subject_in_table = True
                        break
                if not subject_in_table:
                    current_subject = Subject(row[1], int(row[2]))
                    self.subject_table.append(current_subject)
            self.grade_table.append(
                Grade(float(row[0]), current_subject, float(row[3]))
            )

    def calculate_total_grade_average(self) -> float:
        """
        Method calculates average grade of all subjects.
        :return: average grade as float value
        """
        grade_total: float = 0
        total_ects: float = 0
        for subject in self.subject_table:
            total_ects += subject.ects_value
            grade_total += (
                self.calculate_subject_average(subject.name) * subject.ects_value
            )
        return grade_total / total_ects

    def calculate_subject_average(self, subject_name: str) -> float:
        """
        Method calculates average grade for specified subject
        :param subject_name: name of a subject which average is calculated
        :return: average subject grade as a float value
        """
        grade_total: float = 0
        grade_total_weights: float = 0
        for grade in self.grade_table:
            if grade.subject.name == subject_name:
                grade_total += grade.value * grade.weight
                grade_total_weights += grade.weight
        return grade_total / grade_total_weights
