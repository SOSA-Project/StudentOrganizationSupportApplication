"""
File contains tests for grade_monitor file.
"""

import pytest
import numpy as np
from numpy import ndarray

from app.backend.grade_monitor import GradeMonitor
from app.backend.grade import Grade
from app.backend.subject import Subject


@pytest.fixture
def sample_grades() -> ndarray:
    """
    Provides a sample numpy array representing grades data for testing.
    :return: Array of grades data for testing.
    """
    return np.array([
        [4.0, "Math", 5, 1],
        [5.0, "Math", 5, 2],
        [3.0, "Physics", 4, 1],
        [4.0, "Physics", 4, 2],
    ])

def test_fill_monitor_tables(sample_grades: np.ndarray) -> None:
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

def test_calculate_subject_average(sample_grades: np.ndarray) -> None:
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

def test_calculate_total_grade_average(sample_grades: np.ndarray) -> None:
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
    empty_array = np.array([])
    monitor = GradeMonitor(empty_array)
    assert monitor.grade_table == []
    assert monitor.subject_table == []
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_total_grade_average()


def test_subject_with_zero_ects() -> None:
    """
    Tests behavior with 0 ects.
    :return: Nothing, only provides test.
    """
    grades_array = np.array([
        [5.0, "Chemistry", 0, 1],
    ])
    monitor = GradeMonitor(grades_array)
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_total_grade_average()


def test_grade_with_zero_weight() -> None:
    """
    Tests behavior with 0 weight.
    :return: Nothing, only provides test.
    """
    grades_array = np.array([
        [5.0, "Biology", 5, 0],
    ])
    monitor = GradeMonitor(grades_array)
    with pytest.raises(ZeroDivisionError):
        monitor.calculate_subject_average("Biology")
