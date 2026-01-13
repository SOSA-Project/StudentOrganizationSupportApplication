"""
File contains tests for grade_monitor file.
"""

import pytest
import numpy as np

from unittest.mock import patch

from app.backend.database import Db
from app.backend.grade_monitor import Grade, GradeMonitor, GradeType, Subject, initiate_grade_monitor


@pytest.fixture
def sample_grades() -> list[tuple[float, str, int, float, int, int]]:
    """
    Provides a sample numpy array representing grades data for testing.
    :return: Array of grades data for testing.
    """
    return [
        (4.0, "Math", 5, 1, 2, 0),
        (5.0, "Math", 5, 2, 1, 1),
        (3.0, "Physics", 4, 1, 1, 2),
        (4.0, "Physics", 4, 2, 2, 3),
    ]


def test_fill_monitor_tables(sample_grades: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests fill_monitor_tables function.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    subject_names = [s.name for s in monitor.subject_table]
    assert "Math" in subject_names
    assert "Physics" in subject_names
    assert len(monitor.grade_table) == 4
    assert all(isinstance(g, Grade) for g in monitor.grade_table)
    for subj in monitor.subject_table:
        assert all(isinstance(gt, GradeType) for gt in subj.grade_types)


def test_calculate_subject_average(sample_grades: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests calculate_subject_average function.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    math_avg = monitor.calculate_subject_average("Math")
    physics_avg = monitor.calculate_subject_average("Physics")
    assert pytest.approx(math_avg, 0.001) == 4.6667
    assert pytest.approx(physics_avg, 0.001) == 3.6667


def test_calculate_subject_average_ignore_ects(sample_grades: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests calculate_subject_average with ignore_ects=True.
    Should compute weighted average ignoring ECTS.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades, ignore_ects=True)
    math_avg = monitor.calculate_subject_average("Math")
    physics_avg = monitor.calculate_subject_average("Physics")
    expected_math = (4 * 1 + 5 * 2) / (1 + 2)
    expected_physics = (3 * 1 + 4 * 2) / (1 + 2)
    assert pytest.approx(math_avg, 0.001) == expected_math
    assert pytest.approx(physics_avg, 0.001) == expected_physics


def test_calculate_total_grade_average(sample_grades: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests calculate_total_grade_average function.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    total_avg = monitor.calculate_total_grade_average()
    assert pytest.approx(total_avg, 0.01) == 4.22


def test_calculate_total_grade_average_ignore_ects(
    sample_grades: list[tuple[float, str, int, float, int, int]],
) -> None:
    """
    Tests calculate_total_grade_average with ignore_ects=True.
    Should treat all ECTS as 1.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades, ignore_ects=True)
    total_avg = monitor.calculate_total_grade_average()
    expected = ((4.0 * 1 + 5.0 * 2) / 3 + (3.0 * 1 + 4.0 * 2) / 3) / 2
    assert pytest.approx(total_avg, 0.001) == expected


def test_empty_grades() -> None:
    """
    Tests empty grades list.
    :return: Nothing, only provides test.
    """
    empty_array: list = []
    monitor = GradeMonitor(empty_array)
    assert monitor.grade_table == []
    assert monitor.subject_table == []
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_total_grade_average()
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_subject_average("Math")


@pytest.mark.parametrize(
    "array",
    [
        (
            np.array(
                [
                    [5.0, "Chemistry", 0, 1, 1, 0],
                ]
            )
        ),
    ],
)
def test_subject_grade_with_zero_value(array: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests behavior with 0 ects.
    :param array: numpy array for tests.
    :return: Nothing, only provides test.
    """

    monitor = GradeMonitor(array)
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_total_grade_average()


def test_calculate_subject_type_average_correct(sample_grades) -> None:
    """
    Tests the calculate_subject_type_average method for correct computation
    of averages and weights for each grade type within a subject.
    :param sample_grades: sample grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    result = monitor.calculate_subject_type_average("Math")

    assert GradeType.WYK in result
    assert GradeType.LAB in result
    assert pytest.approx(result[GradeType.WYK][0], 0.01) == 5.0
    assert pytest.approx(result[GradeType.LAB][0], 0.01) == 4.0
    assert result[GradeType.WYK][1] == 2.0
    assert result[GradeType.LAB][1] == 1.0


def test_calculate_subject_type_average_empty_subject(sample_grades) -> None:
    """
    Tests the calculate_subject_type_average method for a non-existent
    subject - Expects to return an empty dictionary.
    :param sample_grades: sample grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    result = monitor.calculate_subject_type_average("Biology")
    assert result == {}


def test_calculate_subject_type_average_with_invalid_weights() -> None:
    """
    Tests the calculate_subject_type_average method for cases with invalid weights
    (zero or negative) - Expects to use the minimum weight found among grades.
    :return: Nothing, only provides test.
    """
    fake_subject = Subject("Test", 5)
    monitor = GradeMonitor([])
    monitor.grade_table = [
        Grade(1, 5.0, fake_subject, 1.0, 1),
        Grade(2, 4.0, fake_subject, 0.0, 1),
        Grade(3, 3.0, fake_subject, -1.0, 1),
    ]

    result = monitor.calculate_subject_type_average("Test")

    assert GradeType.WYK in result
    assert pytest.approx(result[GradeType.WYK][0], 0.01) == 4.0
    assert result[GradeType.WYK][1] == -1.0


def test_calculate_subject_type_average_with_single_grade(sample_grades) -> None:
    """
    Tests the calculate_subject_type_average method for subjects with only one
    grade per type. Ensures averages and weights are computed correctly.
    :param sample_grades: sample grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    result = monitor.calculate_subject_type_average("Physics")

    assert len(result) == 2
    assert GradeType.WYK in result
    assert GradeType.LAB in result
    assert pytest.approx(result[GradeType.WYK][0], 0.01) == 3.0
    assert pytest.approx(result[GradeType.LAB][0], 0.01) == 4.0
    assert result[GradeType.WYK][1] == 1.0
    assert result[GradeType.LAB][1] == 2.0


def test_grade_counts(sample_grades: list[tuple[float, str, int, float, int, int]]) -> None:
    """
    Tests grade_counts function.
    :param sample_grades: sample grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    counts_all = monitor.grade_counts()
    assert counts_all[4.0] == 2
    assert counts_all[5.0] == 1
    assert counts_all[3.0] == 1
    counts_math = monitor.grade_counts(["Math"])
    assert counts_math[4.0] == 1
    assert counts_math[5.0] == 1
    counts_nonexistent = monitor.grade_counts(["Biology"])
    assert counts_nonexistent == {}


def test_initiate_grade_monitor_success() -> None:
    """
    Tests initiate_grade_monitor function for the successful creation of a GradeMonitor instance.
    Mocks fetch_grades to return valid grade data.
    Checks that the returned object is an instance of GradeMonitor and contains correct number of grades.
    :return: Nothing, only provides test.
    """
    fake_data = [(4.0, "Math", 5, 1.0, 2, 0)]
    with patch.object(Db, "fetch_grades", return_value=fake_data):
        monitor = initiate_grade_monitor()
        assert isinstance(monitor, GradeMonitor)
        assert len(monitor.grade_table) == 1


def test_initiate_grade_monitor_invalid_data() -> None:
    """
    Tests initiate_grade_monitor function with invalid data returned from fetch_grades.
    Mocks fetch_grades to return a string instead of a list.
    The function should return None for invalid input.
    :return: Nothing, only provides test.
    """
    invalid_data = "not a list"
    with patch.object(Db, "fetch_grades", return_value=invalid_data):
        monitor = initiate_grade_monitor()
        assert monitor is None


def test_initiate_grade_monitor_type_error() -> None:
    """
    Tests initiate_grade_monitor function handling of exceptions.
    Mocks fetch_grades to raise TypeError.
    The function should catch the exception and return None.
    :return: Nothing, only provides test.
    """
    with patch.object(Db, "fetch_grades", side_effect=TypeError):
        monitor = initiate_grade_monitor()
        assert monitor is None
        monitor = initiate_grade_monitor()
        assert monitor is None
