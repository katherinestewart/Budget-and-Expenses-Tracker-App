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

    target_y = []

    # list of constant target value to create target line
    for _ in y_coords:
        target_y.append(target)

    x = np.array(x_coords)
    y = np.array(y_coords)

    plt.figure(figsize=(8, 6))
    plt.title(f"{labels[0]} Progress for {year}")
    plt.xlabel("Weeks")
    plt.ylabel("Amount (£)")

    # Plot scatter graph of total amount for each week
    plt.scatter(x, y, color="r", label=f"Weekly {labels[1]}")

    # Plot line y = target
    y = np.array(target_y)
    plt.plot(x, y, color="g", label=f"{labels[2]}")

    # Plot line of best fit of average income or spending so far for
    # each week in year
    y = np.array(av_y)
    a, b = np.polyfit(x, y, 1)
    plt.plot(x, a * x + b, color="b", label=f"Average {labels[1]}")

    plt.legend()

    plt.show()
    cf.clear()
