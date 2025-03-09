"""This module gets all arguments to create a graph showing progress
for a financial goal."""

from functions import date_functions as df
from database import database_commands as dc
from maths import calculations as calc, graphs
from maths.calculations import difference as diff


def get_gross_args():
    """This function gets all arguments specific to the progress in the
    annual gross income goal.

    :return: target gross, total gross for each week, average gross
    :rtype: float, list, list
    """
    dates_list = df.get_date_of_first_day_each_week_this_year()
    y_coordinates = get_income_for_week(dates_list)
    averages = get_average_so_far_for_each_week_in_year(y_coordinates)

    # Get annual goal amount
    goals_list = dc.get_row_list("goals")
    annual_amount = None
    for row in goals_list:
        if row[1] == "gross income":
            annual_amount = row[2]

    gross_target = calc.get_week_from_year(annual_amount)

    return gross_target, y_coordinates, averages


def get_budget_args():
    """This function gets the arguments specific to the progress in the
    annual budget goal.

    :return: weekly budget, total spent in each week, average spent
    :rtype: float, list, list
    """
    dates_list = df.get_date_of_first_day_each_week_this_year()
    y_coordinates = get_spending_for_week(dates_list)
    averages = get_average_so_far_for_each_week_in_year(y_coordinates)

    # Get annual budget amount
    goals_list = dc.get_row_list("goals")
    annual_amount = None

    for row in goals_list:
        if row[1] == "budget" and row[3] == "annual":
            annual_amount = row[2]

    budget_target = calc.get_week_from_year(annual_amount)

    return budget_target, y_coordinates, averages


def get_net_args():
    """This function gets all arguments specific to the progress in the
    annual net income goal.

    :return: target net, total net for each week, average net
    :rtype: float, list, list
    """
    gross_target, gross_y_coordinates, gross_averages = get_gross_args()
    budget_target, budget_y_coordinates, budget_averages = get_budget_args()
    net_target = diff(budget_target, gross_target)

    # Get net income for each week
    y_coordinates = []
    for i, y_coordinate in enumerate(gross_y_coordinates):
        amount = diff(budget_y_coordinates[i], y_coordinate)
        y_coordinates.append(amount)

    # Get average income for year so far for each week
    averages = []
    for i, budget_average in enumerate(budget_averages):
        average = diff(budget_average, gross_averages[i])
        averages.append(average)

    return net_target, y_coordinates, averages


def get_common_args():
    """This function gets the arguments to create a graph showing
    progress towards a financial goal which are common to all goals.

    :param goal: 'net income', 'gross income' or 'budget'
    :return: None
    """
    dates_list = df.get_date_of_first_day_each_week_this_year()
    year = dates_list[-1]
    year = year.strftime("%Y-%m-%d")[:4]

    # Get list of integers for each date in dates_list
    x_coordinates = get_x_coordinates(dates_list)
    return year, x_coordinates


def get_x_coordinates(dates_list):
    """This function takes in a list of dates and returns a list
    with a week number for each date.

    :param dates_list: list of dates
    :return: list of numbers for each week in year so far
    :rtype: list of int
    """
    x_coords = []
    for i, _ in enumerate(dates_list):
        x_coords.append(i + 1)
    return x_coords


def create_gross_income_graph():
    """This function calls the function to create a graph with the
    arguments to show progress towards annual gross income goal.

    :return: None
    """
    labels = get_labels("gross income")
    graphs.make_plot(get_common_args(), get_gross_args(), labels)


def create_net_income_graph():
    """This function calls the function to create a graph with the
    arguments to show progress towards annual net income goal.

    :return: None
    """
    labels = get_labels("net income")
    graphs.make_plot(get_common_args(), get_net_args(), labels)


def create_budget_graph():
    """This function calls the function to create a graph with the
    arguments to show progress towards annual budget goal.

    :return: None
    """
    labels = get_labels("budget")
    graphs.make_plot(get_common_args(), get_budget_args(), labels)


def get_amount_from_rows(row_list):
    """This function takes in a list of rows from expenses or income
    tables and returns a list of their amounts

    :param row_list: list of rows from table
    :return: list of amounts
    :rtype: list of floats
    """
    amounts = []
    for row in row_list:
        amounts.append(float(row[3]))
    return amounts


def get_spending_for_week(dates_list):
    """This function gets the total spending for each week from a list
    of dates.

    :param dates_list: list of dates of start of each week this year
    :return: list of total spend for each week
    :rtype: list of floats
    """
    spending = []

    for date in dates_list:
        dates_in_week = df.all_dates_in_week(date)
        spending_wk = dc.get_expenses_by_date(dates_in_week)
        amounts = get_amount_from_rows(spending_wk)
        total = calc.total_spending(amounts)
        spending.append(total)

    return spending


def get_income_for_week(dates_list):
    """This function gets the total income for each week in a list of
    dates.

    :param dates_list: list of dates of start of each week this year
    :return: list of total income for each week
    :rtype: list of floats
    """
    income = []

    for date in dates_list:
        dates_in_week = df.all_dates_in_week(date)
        incomes_over_week = dc.get_income_by_date(dates_in_week)
        amounts = get_amount_from_rows(incomes_over_week)
        total = calc.total_spending(amounts)
        income.append(total)

    return income


def get_average_so_far_for_each_week_in_year(amount_list):
    """This function gets the average amount spent or earned so far
    this year on the first day of each week of the year.

    :param amount_list: list of floats
    :return: cumulative averages
    :rtype: list
    """
    average_list = []

    for i, _ in enumerate(amount_list):
        number = calc.get_mean(amount_list[: i + 1])
        number = round(number, 2)
        average_list.append(number)

    return average_list


def get_labels(goal):
    """This function gets the labels to plot graph according to goal.

    :param goal: 'net income', 'gross income', 'budget
    :return: labels
    :rtype: tuple of str
    """
    if goal == "gross income":
        goal = "Gross Income"
        l1 = "income"
        l2 = "Target"
    elif goal == "net income":
        goal = "Net Income"
        l1 = "net income"
        l2 = "Target"
    else:
        goal = "Budget"
        l1 = "expenditure"
        l2 = "Budget"
    return (goal, l1, l2)
