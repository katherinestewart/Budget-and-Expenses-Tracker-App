"""This module contains the goals menu. It gets user choice to set
financial goals; by net or gross income, weekly, monthly or annually,
view progress towards financial goals; for gross income, net income or
budget and cancel; return to main menu. It also contains all relevant
functions to get the required returns for each selection.
"""

from functions import common_functions as cf, date_functions as df
from database import database_commands as dc
from maths import calculations as calc
from menu import budget
from menu import create_graph as cg

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
            amount = calc.annual_from_weekly(amount)
        if term == "monthly":
            amount = calc.annual_from_monthly(amount)

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
    new_net = calc.difference(current_budget, new_gross)
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


def view_progress():
    """This function handles the progress menu and calls the relevant
    functions from user choice

    :return: None
    """
    while True:
        menu_sel = input(PROGRESS_MENU).strip().replace(".", "")

        if menu_sel == "1":
            cg.create_gross_income_graph()
        elif menu_sel == "2":
            cg.create_net_income_graph()
        elif menu_sel == "3":
            cg.create_budget_graph()
        elif menu_sel == "0":
            break
        else:
            print(cf.INVALID_INPUT)

    cf.clear()


def get_no_weeks():
    """This function gets a list of integers corresponding to the
    length of a list of dates.  This is for the x-coordinates for
    plotting graph.

    :return: list of integers
    :rtype: list of int
    """
    # Get a list of first date in each week
    dates_list = df.get_date_of_first_day_each_week_this_year()
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
