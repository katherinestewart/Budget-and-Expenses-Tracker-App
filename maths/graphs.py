"""This module plots a graph to show progress in a financial goal. For
a budget; it plots a scatter graph with the total spending for each
week in the year so far, it draws a line of best fit for the cumulative
average spending for each week and it draws a horizontal line for the
target budget.  Similarly, for gross or net income it plots income in
a scatter graph, draws a line showing the cumulative average income for
each week and a horizontal line showing the target income.
"""

from matplotlib import pyplot as plt
import numpy as np
from functions import common_functions as cf


def make_plot(common_args, goal_args, labels):
    """This function plots a graph to show progress in a financial
    goal

    :param common_args: tuple with arguments common to all goals
    :param goal_args: tuple with goal-specific arguments
    :param labels: tuple with strings for labels relevant to goal
    :return: None
    """
    year, x_coords = common_args
    target, y_coords, av_y = goal_args

    plt.style.use("seaborn-v0_8-paper")
    _, ax = plt.subplots()
    plt.title(f"{labels[0]} Progress for {year}")
    plt.xlabel("Weeks")
    plt.ylabel("Amount (£)")

    x = np.array(x_coords)
    y = np.array(y_coords)


    # Plot scatter graph of total amount for each week
    ax.scatter(x, y, color="r", label=f"Weekly {labels[1]}")

    # Plot line of best fit of average income or spending so far for
    # each week in year
    y = np.array(av_y)
    a, b = np.polyfit(x, y, 1)
    y2 = a * x + b
    ax.plot(x, y2, color="b", label=f"Average {labels[1]}")

    # Plot line y = target
    y1 = target

    ax.axhline(y=target, color="g", label=f"{labels[2]}")

    if labels[0] == "Budget":
        ax.fill_between(x, y1, y2, where=(y2 > y1), color="r", alpha=0.2, interpolate=True)
        ax.fill_between(x, y2, y1, where=(y2 <= y1), color="g", alpha=0.2, interpolate=True)
    else:
        ax.fill_between(x, y1, y2, where=(y2 < y1), color="r", alpha=0.2, interpolate=True)
        ax.fill_between(x, y1, y2, where=(y2 > y1), color="g", alpha=0.2, interpolate=True)

    plt.legend()

    plt.show()
    cf.clear()
