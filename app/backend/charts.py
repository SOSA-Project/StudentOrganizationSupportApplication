"""
This file contains functions that creates plots
"""

from typing import Callable
import matplotlib.pyplot as plt
from collections import Counter

from app.backend.grade_monitor import GradeMonitor

monitor = GradeMonitor([(3, "polski", 4, 2), (5, "matematyka", 3, 1), (2, "historia", 5, 2), (5, "polski", 4, 2)])

def histogram_plot(grades: dict[float, int], theme: str) -> None:
    """
    Function that creates a histogram plot
    :param grades: dictionary of grades and their count
    :param theme: theme as string
    :return: nothing, only creates a histogram plot
    """
    colors = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]
    plt.rcParams["axes.facecolor"] = "white"

    unique_sorted = sorted(grades.keys())
    labels = [str(g) for g in unique_sorted]
    heights = [grades[g] for g in unique_sorted]
    x = range(len(labels))

    fig = plt.figure(figsize=(10, 6), frameon=False)
    color = "black"

    if theme == "light":
        t_color = "black"
    elif theme == "dark":
        t_color = "white"
        color = "white"
        plt.rcParams["axes.facecolor"] = "#242424"

    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(axis="x", colors=color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)
    ax.spines["bottom"].set_color(color)
    ax.spines["top"].set_color(color)
    ax.spines["left"].set_color(color)
    ax.spines["right"].set_color(color)
    plt.bar(x, heights, color=colors, width=0.5, edgecolor=color)

    plt.xticks(x, labels)
    plt.yticks([])
    plt.xlabel("Grades")
    plt.title("Histogram of Grades")

    for xi, h in zip(x, heights):
        plt.text(xi, h + 0.05, str(h), ha="center", va="center", color=t_color)

    plt.show()


def pie_plot(grades: dict[float, int], theme: str) -> None:
    """
    Function that creates a pie plot
    :param grades: dictionary of grades and their count
    :param theme: theme as string
    :return: nothing, only creates a pie plot
    """
    colors = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]

    values = list(grades.values())

    if theme == "light":
        color = "black"
    elif theme == "dark":
        color = "white"

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


histogram_plot(monitor.grade_counts(), theme="light")
pie_plot(monitor.grade_counts(), theme="dark")