"""
File contains definition for GradeMonitor class, its functionality and definitions of helper classes
"""

from data_base import fetch_grades


class Subject:
    """
    Class stores information about a Subject
    """

    def __init__(self, name: str, ects_value: int) -> None:
        self.name = name
        self.ects_value = ects_value


class Grade:
    """
    Class stores information about a Grade
    """

    def __init__(self, value: float, subject: Subject, weight: float = 1) -> None:
        self.value = value
        self.subject = subject
        self.weight = weight


class GradeMonitor:
    """
    Purpose of the class is to collect, manage and operate of grade data from the database.
    """

    def __init__(self, grades_list: list[tuple[float, str, int, float]]) -> None:
        self.grade_table: list[Grade] = []
        self.subject_table: list[Subject] = []
        self.fill_monitor_tables(grades_list)

    def fill_monitor_tables(self, grades_list: list[tuple[float, str, int, float]]) -> None:
        """
        Method fills monitor's tables with data fetched from database.
        :param grades_list: table of grades data fetched from database
        :return: nothing
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
            self.grade_table.append(Grade(float(row[0]), current_subject, float(row[3])))

    def calculate_total_grade_average(self) -> float:
        """
        Method calculates average grade of all subjects.
        :return: average grade as float value
        """
        grade_total: float = 0
        total_ects: float = 0

        for subject in self.subject_table:
            total_ects += subject.ects_value
            grade_total += self.calculate_subject_average(subject.name) * subject.ects_value
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


def initiate_grade_monitor() -> GradeMonitor | None:
    """
    Function fetches data from database, verifies it and creates an instance of GradeMonitor class for application use
    :return: An instance of GradeMonitor class
    """
    try:
        grades = fetch_grades()
        correct_check: int = 0
        if isinstance(grades, list):
            for item in grades:
                if isinstance(item, tuple):
                    if len(item) == 4:
                        if (
                            isinstance(item[0], float)
                            and isinstance(item[1], str)
                            and isinstance(item[2], int)
                            and isinstance(item[3], int)
                        ):
                            correct_check += 1
        if correct_check == len(grades):
            return GradeMonitor(grades)
        return None
    except TypeError:
        print("Grades could not be fetched from database")
        return None
