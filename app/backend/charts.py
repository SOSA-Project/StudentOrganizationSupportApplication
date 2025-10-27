"""
This file contains functions that creates plots
"""

from typing import Callable
import matplotlib.pyplot as plt

from app.backend.grade_monitor import GradeMonitor


class StatisticsManager:
    """
    Class provides methods to calculate averages and other statistics
    based on GradeMonitor data.
    """

    def __init__(self, monitor: GradeMonitor) -> None:
        self.monitor = monitor

    def subjects_averages(self) -> dict[str, float]:
        """
        Method that calculates the average subject grade
        :return: Dictionary containing subject and the average subject grade
        """
        subjects_averages: dict[str, float] = {
            grade.name: self.monitor.calculate_subject_average(grade.name) for grade in self.monitor.subject_table
        }
        subjects_averages["All subjects"] = self.monitor.calculate_total_grade_average()

        return subjects_averages


def _configure_theme(theme: str) -> tuple[str, str]:
    """
    Function that configures colors based on theme.
    :param theme: 'light' or 'dark'
    :return: Tuple containing colors
    """
    if theme == "dark":
        plt.rcParams["axes.facecolor"] = "#242424"
        return "white", "white"
    else:
        plt.rcParams["axes.facecolor"] = "white"
        return "black", "black"


def _setup_axes(ax: plt.Axes, color: str) -> None:
    """
    Function that configures axes based on color.
    :param ax: Axes object to configure
    :param color: Color of axes
    :return: Nothing, only configures axes
    """
    ax.tick_params(axis="x", colors=color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)
    for side in ["bottom", "top", "left", "right"]:
        ax.spines[side].set_color(color)


def all_grades_histogram_plot(grades: dict[float, int], theme: str) -> None:
    """
    Function that creates a histogram plot of grades
    :param grades: Dictionary of grades and their count
    :param theme: 'light' or 'dark'
    :return: Nothing, only creates a histogram plot
    """
    colors = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]
    t_color, edge_color = _configure_theme(theme)

    unique_sorted = sorted(grades.keys())
    labels = [str(g) for g in unique_sorted]
    heights = [grades[g] for g in unique_sorted]
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(10, 6), frameon=False)
    _setup_axes(ax, edge_color)

    ax.bar(x, heights, color=colors[: len(heights)], width=0.5, edgecolor=edge_color)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Grade", color=edge_color)
    ax.set_title("Histogram of Grades", color=edge_color)
    ax.set_yticks([])

    for xi, h in zip(x, heights):
        ax.text(xi, h + 0.05, str(h), ha="center", va="center", color=t_color)

    plt.show()


def all_grades_pie_plot(grades: dict[float, int], theme: str) -> None:
    """
    Function that creates a pie plot of grades
    :param grades: Dictionary of grades and their count
    :param theme: 'light' or 'dark'
    :return: Nothing, only creates a pie plot
    """
    colors: list[str] = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]

    values = list(grades.values())

    color = _configure_theme(theme)[1]

    def make_autopct(values: list[int]) -> Callable[[float], str]:
        def my_autopct(pct: float) -> str:
            total = sum(values)
            count = int(round(pct * total / 100.0))
            return f"{count}"

        return my_autopct

    plt.figure(figsize=(6, 6), frameon=False)
    plt.pie(
        list(grades.values()),
        labels=[str(k) for k in grades.keys()],
        autopct=make_autopct(values),
        startangle=90,
        colors=colors,
        textprops=dict(color=color),
    )

    plt.title("Pie chart of Grades", color=color)
    plt.show()


def subjects_averages_histogram_plot(averages: dict[str, float], theme: str) -> None:
    """
    Function that creates a histogram plot of subjects averages
    :param averages: Dictionary of subjects and their averages
    :param theme: 'light' or 'dark'
    :return: Nothing, only creates a histogram plot
    """

    t_color, edge_color = _configure_theme(theme)

    unique_sorted = averages.keys()
    labels = [str(g) for g in unique_sorted]
    heights: list[float] = [averages[s] for s in labels]
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(10, 6), frameon=False)
    _setup_axes(ax, edge_color)

    ax.bar(x, heights, width=0.5, edgecolor=edge_color)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Average", color=edge_color)
    ax.set_title("Histogram of Averages", color=edge_color)
    ax.set_yticks([])

    for xi, h in zip(x, heights):
        ax.text(xi, h + 0.05, str(h), ha="center", va="center", color=t_color)

    plt.show()


mon = GradeMonitor(
    [(3, "polski", 4, 2), (5, "matematyka", 3, 1), (2, "historia", 5, 2), (4.5, "polski", 4, 2), (4.5, "polski", 4, 2)]
)

all_grades_histogram_plot(mon.grade_counts(), "light")
all_grades_pie_plot(mon.grade_counts(), "dark")
all_grades_pie_plot(mon.grade_counts(), "light")

stats = StatisticsManager(mon)
# print(mon.calculate_total_grade_average())

subjects_averages_histogram_plot(stats.subjects_averages(), "dark")
