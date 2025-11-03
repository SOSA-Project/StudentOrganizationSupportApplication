"""
File contains definition for GradeMonitor class, its functionality and definitions of helper classes
"""

import math

from app.backend.data_base import fetch_grades
from enum import Enum


class GradeType(Enum):
    """
    Enumerator class for types of grades
    """

    WYK = 1
    LAB = 2
    CW = 3
    SEM = 4


class Subject:
    """
    Class stores information about a Subject
    """

    def __init__(self, name: str, ects_value: int) -> None:
        self.name: str = name
        self.ects_value: int = ects_value
        self.grade_types: list[GradeType] = []


class Grade:
    """
    Class stores information about a Grade
    """

    def __init__(self, grade_id: int, value: float, subject: Subject, weight: float = 1, grade_type: int = 1) -> None:
        self.value: float = value
        self.subject: Subject = subject
        self.weight: float = weight
        self.type: GradeType = GradeType(max(min(grade_type, len(GradeType)), 1))
        self.id = grade_id


class GradeMonitor:
    """
    Purpose of the class is to collect, manage and operate on grade data from the database.
    """

    def __init__(self, grades_list: list[tuple[float, str, int, float, int, int]], ignore_ects: bool = False) -> None:
        self.grade_table: list[Grade] = []
        self.subject_table: list[Subject] = []
        self.fill_monitor_tables(grades_list)
        self.ignore_ects: bool = ignore_ects

    def fill_monitor_tables(self, grades_list: list[tuple[float, str, int, float, int, int]]) -> None:
        """
        Method fills monitor's tables with data fetched from database.
        :param grades_list: Table of grades data fetched from database
        :return: Nothing
        """
        current_subject: Subject = Subject("", 0)

        for row in grades_list:
            if len(self.subject_table) == 0:
                current_subject.name = row[1]
                current_subject.ects_value = row[2]
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

            new_grade = Grade(int(row[5]), float(row[0]), current_subject, float(row[3]), int(row[4]))

            if new_grade.type not in current_subject.grade_types:
                current_subject.grade_types.append(new_grade.type)
            self.grade_table.append(new_grade)

        for subject in self.subject_table:
            subject.grade_types.sort(key=lambda x: x.value)

    def calculate_total_grade_average(self) -> float:
        """
        Method calculates average grade of all subjects.
        :return: Total average grade as float value
        """
        grade_total: float = 0
        total_ects: float = 0
        ects_value: int

        for subject in self.subject_table:
            if self.ignore_ects:
                ects_value = 1
            else:
                ects_value = int(math.fabs(float(subject.ects_value)))
            total_ects += ects_value
            grade_total += self.calculate_subject_average(subject.name) * ects_value

        return grade_total / total_ects

    def calculate_subject_average(self, subject_name: str) -> float:
        """
        Method calculates average grade for specified subject
        :param subject_name: Name of a subject which average is calculated
        :return: Average subject grade as a float value
        """
        if self.ignore_ects:
            return self.calculate_subject_regular_average(subject_name)
        else:
            grade_total: float = 0
            grade_total_weights: float = 0
            subject_types_grades = self.calculate_subject_type_average(subject_name)
            for tp in subject_types_grades.values():
                grade_total += tp[0] * tp[1]
                grade_total_weights += tp[1]
            return grade_total / grade_total_weights

    def calculate_subject_regular_average(self, subject_name: str) -> float:
        """
        Method calculates subject average in a regular grading system with one module per subject with grade weights
        :param subject_name: Name of a subject which average is calculated
        :return: Average subject grade as a float value
        """
        grade_total: float = 0
        grade_total_weights: float = 0
        grade_weight: float
        for grade in self.grade_table:
            if grade.subject.name == subject_name:
                if grade.weight <= 0 or not isinstance(grade.weight, float):
                    grade_weight = 1
                else:
                    grade_weight = grade.weight
                grade_total += grade.value * grade_weight
                grade_total_weights += grade_weight
        return grade_total / grade_total_weights

    def calculate_subject_type_average(self, subject_name: str) -> dict[GradeType, tuple[float, float]]:
        """
        Method returns averages for a specified subject for each type of grade in a dictionary form
        with weight of type attached
        :param subject_name: Name of a subject of which grade type averages are calculated
        :return: Dictionary of a subject grade type and a tuple containing its average and weight
        """
        type_averages: dict[GradeType, tuple[float, float]] = {}
        type_counts: dict[GradeType, int] = {}

        for grade in self.grade_table:
            if grade.subject.name == subject_name:
                averages = type_averages.get(grade.type, (0.0, grade.weight))
                type_averages[grade.type] = (averages[0] + grade.value, min(averages[1], grade.weight))
                type_counts[grade.type] = type_counts.get(grade.type, 0) + 1

        for tp in type_averages:
            averages = type_averages[tp]
            type_averages[tp] = (averages[0] / type_counts[tp], averages[1])

        return type_averages

    def grade_counts(self, subject_names=None) -> dict[float, int]:
        """
        Method counts quantity of each grade, possible filtering by subject name
        :param subject_names: Optional parameter - names of subjects to count grades from
        :return: Dictionary containing counts of each grade
        """
        if subject_names is None:
            subject_names = []

        grade_count: dict[float, int] = {}
        for grade in self.grade_table:
            if len(subject_names) == 0:
                grade_count[grade.value] = grade_count.get(grade.value, 0) + 1
            elif grade.subject.name in subject_names:
                grade_count[grade.value] = grade_count.get(grade.value, 0) + 1

        return grade_count


def initiate_grade_monitor(ignore_ects: bool = False) -> GradeMonitor | None:
    """
    Function fetches data from database, verifies it and creates an instance of GradeMonitor class for application use
    :param ignore_ects: Optional parameter - if set to true the monitor class will ignore ects values of subjects
    :return: An instance of GradeMonitor class
    """
    try:
        grades = fetch_grades()
        if not grades or not isinstance(grades, list):
            return None

        def valid_item(item: tuple) -> bool:
            expected_types = (float, str, int, float, int, int)
            if not isinstance(item, tuple) or len(item) != len(expected_types):
                return False
            return all(isinstance(x, t) for x, t in zip(item, expected_types))

        if all(valid_item(item) for item in grades):
            return GradeMonitor(grades, ignore_ects)

        return None

    except TypeError:
        print("Grades could not be fetched from database")
        return None
