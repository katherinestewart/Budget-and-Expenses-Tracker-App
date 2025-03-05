"""This module contains the goals menu. It gets user choice to set
financial goals; by net or gross income, weekly, monthly or annually,
view progress towards financial goals; for gross income, net income or
budget and cancel; return to main menu. It also contains all relevant
functions to get the required returns for each selection.
"""

from functions import common_functions as cf, date_functions as df
from database import database_commands as dc
from maths import calcs, graphs
from menu import budget

SET_GOAL_MENU = """\n\U000026bd Please choose from the following options:
\n1.  Set gross income goal
2.  Set net income goal
0.  Cancel set goal
\nEnter you selection: \
"""
DATE_MENU = """\U0001f4c5 Please choose from the following options:
\n1.  Weekly amount
2.  Monthly amount
3.  Annual amount
0.  Cancel set amount
\nEnter you selection: \
"""
SEL = "\033[36m\033[1m -------- \033[0m\033[1m"
END = "\033[36m\033[1m --------\033[0m"
MENU_TITLE = f"\U0001f90c {SEL}FINANCIAL GOALS{END}"
GOALS_MENU = f"""{MENU_TITLE}
\nPlease choose from the following options:
\n1.  Set financial goals
2.  View progress towards financial goals
0.  Cancel
\nEnter you selection: \
"""
PROGRESS_MENU = """\U0001f945 View progress for:
\n1.  Gross Income
2.  Net Income
3.  Budget
0.  Cancel
\nEnter you selection: \
"""
INVALID_INPUT = "\nYou entered an invalid input.  Please try again."
SEL_ = cf.SEL_
END_ = cf.END_
SELECT_1 = f"{SEL_}Set Financial Goals{END_}"
SELECT_2 = f"{SEL_}View Progress{END_}"


def set_financial_goals(gross_or_net):
    """This function sets a financial goal for gross or net income for
    user's selected term.

    :param gross_or_net: str 'gross income' or 'net income'
    :return: None
    """
    term = cf.get_term(DATE_MENU)

    if term:
        amount = float(cf.get_amount())
        if term == "weekly":
            amount = calcs.annual_from_weekly(amount)
        if term == "monthly":
            amount = calcs.annual_from_monthly(amount)

        # User selected gross income goal
        if gross_or_net == "1":
            update_gross_income(amount)

        # User selected net income goal
        if gross_or_net == "2":
            update_net_income(amount)


def update_gross_income(new_gross):
    """This function updates values in budget table for a new gross
    income

    :param new_gross: amount for new gross income
    :return: None
    """
    current_budget = get_annual("budget")
    new_net = calcs.difference(current_budget, new_gross)
    dc.enter_goal("gross income", new_gross, "annual")

    if new_net >= 0:
        dc.enter_goal("net income", new_net, "annual")

    # Net income cannot be negative. Adjust gross income goal.
    else:
        dc.enter_goal("net income", 0, "annual")
        budget.update_overall_budgets("annual", new_gross)

    cf.clear()
    print("\nGoal has been added \U00002705\n")


def update_net_income(new_net):
    """This function updates values in budget table for a new net
    income

    :param new_net: amount for new net income
    :return: None
    """
    current_gross = get_annual("gross income")
    new_budg = current_gross - new_net
    dc.enter_goal("net income", new_net, "annual")

    #  Gross income cannot be less than net.  Adjust gross.
    if new_net >= current_gross:
        dc.enter_goal("gross income", new_net, "annual")

    budget.update_overall_budgets("annual", new_budg)
    print("Goal has been added \U00002705\n")


def get_gross_or_net():
    """This function gets user choice for setting a financial goal

    :return: 'gross income' or 'net income'
    :rtype: str
    """
    while True:
        gross_or_net = input(SET_GOAL_MENU).strip().replace(".", "")

        if gross_or_net in ("0", "1", "2"):
            return gross_or_net

        print(cf.INVALID_INPUT)


def get_annual(goal):
    """This function gets annual goal

    :param goal: 'gross income' or 'net income'
    :return: amount of money or None
    :rtype: float or None
    """
    goals_list = dc.get_row_list("goals")

    for row in goals_list:
        if row[1] == goal:
            return float(row[2])
    return None


def get_spending_for_week(dates_list):
    """This function gets the total spending for each week in a list

    :param dates_list: list of dates of start of each week this year
    :return: list of total spend for each week
    :rtype: list of floats
    """
    spending = []

    for date in dates_list:
        dates_in_week = df.get_dates_in_week(date)
        spending_wk = dc.get_expenses_by_date(dates_in_week)
        amounts = get_amount_from_rows(spending_wk)
        total = calcs.total_spending(amounts)
        spending.append(total)

    return spending


def get_income_for_week(dates_list):
    """This function gets the total income for each week in a list

    :param dates_list: list of dates of start of each week this year
    :return: list of total income for each week
    :rtype: list of floats
    """
    income = []

    for date in dates_list:
        dates_in_week = df.get_dates_in_week(date)
        income_wk = dc.get_income_by_date(dates_in_week)
        amounts = get_amount_from_rows(income_wk)
        total = calcs.total_spending(amounts)
        income.append(total)

    return income


def get_amount_from_rows(amount_list):
    """This function takes in a list of rows from expenses or income
    tables and returns a list of their amounts

    :param expenses_list: list of rows from expenses table
    :return: list of amounts
    :rtype: list of floats
    """
    amounts = []
    for row in amount_list:
        amounts.append(float(row[3]))
    return amounts


def get_x_coords(dates_list):
    """This function takes in a list of dates and returns a list
    with a week number for each date

    :param dates_list: list of dates
    :return: list of numbers for each week in year so far
    :rtype: list of int
    """
    x_coords = []
    for i, _ in enumerate(dates_list):
        x_coords.append(i + 1)
    return x_coords


def view_progress():
    """This function handles the progress menu and calls the relevant
    functions from user choice

    :return: None
    """
    while True:
        menu_sel = input(PROGRESS_MENU).strip().replace(".", "")
        dates_list = df.get_year_weeks()

        if menu_sel == "1":
            goal = "gross income"
            goal_args = get_gross_args(dates_list)
        elif menu_sel == "2":
            goal = "net income"
            goal_args = get_net_args(dates_list)
        elif menu_sel == "3":
            goal = "budget"
            goal_args = get_budget_args(dates_list)
        elif menu_sel == "0":
            break
        else:
            print(cf.INVALID_INPUT)

        get_graph(goal, dates_list, goal_args)
    cf.clear()


def get_labels(goal):
    """This function gets the labels to plot graph according to goal

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


def get_budget_args(dates_list):
    """This function gets the arguments to plot a graph to view
    progress for a budget goal

    :param dates_list: list of dates
    :return: target = target, y_coords, average for each coordinate
    :rtype: float, list, list
    """
    # Get spending for each week starting on date in date list
    y_coords = get_spending_for_week(dates_list)

    # Get mean average weekly spend so far for each week
    average_y = calcs.get_average_amount(y_coords)

    # Get annual budget amount
    goals_list = dc.get_row_list("goals")
    annual_amount = None

    for row in goals_list:
        if row[1] == "budget" and row[3] == "annual":
            annual_amount = row[2]

    target = calcs.get_week_from_year(annual_amount)

    return target, y_coords, average_y


def get_gross_args(dates_list):
    """This function gets the arguments to plot a graph to view
    progress for a gross income goal

    :param dates_list: list of dates
    :return: target = target and net income, average income for each week
    :rtype: float, list, list
    """
    # Get income for each week starting on date in date list
    y_coords = get_income_for_week(dates_list)

    # Get average weekly spend so far for each week
    average_y = calcs.get_average_amount(y_coords)

    # Get annual goal amount
    goals_list = dc.get_row_list("goals")
    annual_amount = None
    for row in goals_list:
        if row[1] == "gross income":
            annual_amount = row[2]

    target = calcs.get_week_from_year(annual_amount)

    return target, y_coords, average_y


def get_net_args(dates_list):
    """This function gets the arguments to plot a graph to view
    progress for a net income goal

    :param dates_list: list of dates
    :return: target and net income, average income for each week
    :rtype: float, list, list
    """
    gross_targ, gross_y_coords, gross_av_y = get_gross_args(dates_list)
    budg_targ, budg_y_coords, budg_av_y = get_budget_args(dates_list)
    target = calcs.difference(budg_targ, gross_targ)

    # Get net income for each week
    y_coords = []
    for i, _ in enumerate(gross_y_coords):
        amount = calcs.difference(budg_y_coords[i], gross_y_coords[i])
        y_coords.append(amount)

    # Get average income for year so far for each week
    average_y = []
    for i, _ in enumerate(budg_av_y):
        average = calcs.difference(budg_av_y[i], gross_av_y[i])
        average_y.append(average)

    return target, y_coords, average_y


def get_graph(goal, dates_list, goal_args):
    """This function gets all arguments calls function to plot graph to
    view progress for a financial goal

    :param goal: 'budget', 'net income' or 'gross income'
    :param dates_list: list of dates
    :param goal_args: target, ycoords list, list of average for coord
    :return: None
    """
    labels = get_labels(goal)
    common_args = get_common_args(dates_list)
    graphs.make_plot(common_args, goal_args, labels)


def get_common_args(dates_list):
    """This function gets the graph for the relevant goal

    :param goal: 'net income', 'gross income' or 'budget'
    :return: None
    """
    year = dates_list[-1]
    year = year.strftime("%Y-%m-%d")[:4]

    # Get list of integers for each date in dates_list
    x_coords = get_x_coords(dates_list)
    return year, x_coords


def get_no_weeks():
    """This function gets a list of integers corresponding to the
    length of a list of dates.  This is for the x-coordinates for
    plotting graph.

    :return: list of integers
    :rtype: list of int
    """
    # Get a list of first date in each week
    dates_list = df.get_year_weeks()
    no_weeks = []

    for i, _ in enumerate(dates_list):
        no_weeks.append(i + 1)
    return no_weeks


def goals_menu():
    """This function gets user selection for the financial goals menu
    and calls relevant functions according to user choice

    :return: None
    """
    while True:
        menu = input(GOALS_MENU).strip().replace(".", "")
        print()

        # ****** Set financial goals ******
        if menu == "1":
            cf.clear()
            print(SELECT_1)
            gross_or_net = get_gross_or_net()

            if gross_or_net in ("1", "2"):
                cf.clear()
                set_financial_goals(gross_or_net)
            cf.clear()

        # ****** View progress towards financial goals ******
        elif menu == "2":
            cf.clear()
            print(SELECT_2)
            print()
            view_progress()

        # ****** Return to main menu ******
        elif menu == "0":
            cf.clear()
            break

        # ****** Add expense ******
        else:
            print(cf.INVALID_INPUT)
    cf.clear()
