import matplotlib.pyplot as plt
from collections import Counter

#plt.rcParams['axes.facecolor'] = '#242424'
colors = ["red", "darkgreen", "green", "forestgreen", "limegreen", "lime"]

gradest = [2, 3, 3.5, 4, 4.5, 5, 3.5, 4, 4.5, 5, 4.5, 2]

# HISTOGRAM
def histogram_plot(grades: list[float], theme: str) -> None:
    """

    :param grades:
    :param theme:
    :return:
    """
    plt.rcParams['axes.facecolor'] = 'white'
    grade_counts = Counter(grades)
    unique_sorted = sorted(grade_counts.keys())
    labels = [str(g) for g in unique_sorted]
    heights = [grade_counts[g] for g in unique_sorted]
    x = range(len(labels))

    fig = plt.figure(figsize=(10, 6), frameon=False)
    color = 'black'

    if theme == "light":
        t_color = "black"

    if theme == "dark":
        t_color = "white"
        color = "white"
        plt.rcParams['axes.facecolor'] = '#242424'

    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(axis='x', colors=color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.spines['right'].set_color(color)
    plt.bar(x, heights, color=colors, width=0.5, edgecolor=color)

    plt.xticks(x, labels)
    plt.yticks([])
    plt.xlabel("Grades")
    plt.title("Histogram of Grades")

    for xi, h in zip(x, heights):
        plt.text(xi, h + 0.05, str(h), ha="center", va="center", color=t_color)

    plt.show()


# PIE CHART
def pie_plot(grades: list[float], theme: str) -> None:
    """

    :param grades:
    :param theme:
    :return:
    """
    grade_counts = Counter(grades)
    values = list(grade_counts.values())

    if theme == "light":
        color = 'black'

    if theme == "dark":
        color = 'white'

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            count = int(round(pct * total / 100.0))
            return f"{count}"

        return my_autopct

    plt.figure(figsize=(6, 6),  frameon=False)
    plt.pie(
        grade_counts.values(),
        labels=[str(k) for k in grade_counts.keys()],
        autopct=make_autopct(values),
        startangle=90,
        colors=colors,
        textprops=dict(color=color),
    )

    plt.title("Pie chart of Grades")
    plt.show()


#histogram_plot(gradest, 'dark')
#histogram_plot(gradest, 'light')
pie_plot(gradest, 'light')
pie_plot(gradest, 'dark')
#line_plot(grades)
