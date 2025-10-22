import matplotlib.pyplot as plt
from collections import Counter

plt.rcParams['axes.facecolor'] = '#242424'


grades = [2, 3, 3.5, 4, 4.5, 5, 3.5, 4, 4.5, 5, 4.5, 2]
grade_counts = Counter(grades)

unique_sorted = sorted(grade_counts.keys())
labels = [str(g) for g in unique_sorted]
heights = [grade_counts[g] for g in unique_sorted]
values = list(grade_counts.values())
colors = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]


# HISTOGRAM
def histogram_plot(grades):
    """

    :param grades:
    :return:
    """
    x = range(len(labels))

    plt.figure(figsize=(10, 6), facecolor='#242424') #frameon=False
    plt.bar(x, heights, color=colors, width=0.5, edgecolor="black")
    plt.xticks(x, labels)
    plt.yticks([])
    plt.xlabel("Grades")
    plt.title("Histogram of Grades")

    for xi, h in zip(x, heights):
        plt.text(xi, h + 0.05, str(h), ha="center", va="center")

    plt.show()


# PIE CHART
def pie_plot(grades):

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            count = int(round(pct * total / 100.0))
            return f"{count}"

        return my_autopct

    plt.figure(figsize=(6, 6),  facecolor='#242424')
    plt.pie(
        grade_counts.values(),
        labels=[str(k) for k in grade_counts.keys()],
        autopct=make_autopct(values),
        startangle=90,
        colors=colors,
    )
    plt.title("Pie chart of Grades")
    plt.show()


# LINE CHART
def line_plot(grades):
    x = range(len(labels))
    plt.figure(figsize=(10, 6))
    plt.plot(unique_sorted, values, marker="o", linestyle="-", color="green")

    plt.title("Line chart of Grades")
    plt.xlabel("Grade")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()


histogram_plot(grades)
pie_plot(grades)
#line_plot(grades)
