"""
File contains tests for grade_monitor file.
"""

import pytest
import numpy as np

from app.backend.grade_monitor import GradeMonitor


@pytest.fixture
def sample_grades() -> list[tuple[float, str, int, float]]:
    """
    Provides a sample numpy array representing grades data for testing.
    :return: Array of grades data for testing.
    """
    return [
        (4.0, "Math", 5, 1),
        (5.0, "Math", 5, 2),
        (3.0, "Physics", 4, 1),
        (4.0, "Physics", 4, 2),
    ]


def test_fill_monitor_tables(sample_grades: list[tuple[float, str, int, float]]) -> None:
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


def test_calculate_subject_average(sample_grades: list[tuple[float, str, int, float]]) -> None:
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


def test_calculate_total_grade_average(sample_grades: list[tuple[float, str, int, float]]) -> None:
    """
    Tests calculate_total_grade_average function.
    :param sample_grades: numpy array representing grades data for testing.
    :return: Nothing, only provides test.
    """
    monitor = GradeMonitor(sample_grades)
    total_avg = monitor.calculate_total_grade_average()
    assert pytest.approx(total_avg, 0.001) == 4.2222


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


@pytest.mark.parametrize(
    "array",
    [
        (
            np.array(
                [
                    [5.0, "Chemistry", 0, 1],
                ]
            )
        ),
        (
            np.array(
                [
                    [5.0, "Biology", 5, 0],
                ]
            )
        ),
    ],
)
def test_subject_grade_with_zero_value(array: list[tuple[float, str, int, float]]) -> None:
    """
    Tests behavior with 0 ects.
    :param array: numpy array for tests.
    :return: Nothing, only provides test.
    """

    monitor = GradeMonitor(array)
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_total_grade_average()
