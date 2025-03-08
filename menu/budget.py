"""This module contains the budget menu. It gets user selection to set
overall budget; for week, month or year, set budget by category; for
week month or year, view budgets, view budget progress; for week month
or year or return to main menu.
"""

from time import sleep
from functions import common_functions as cf, date_functions as df
from database import database_commands
from menu import expenses
from maths import calculations

SEL = "\033[36m\033[1m -------- \033[0m\033[1m"
END = "\033[36m\033[1m --------\033[0m"
MENU_TITLE = f"\U0001fa99 {SEL}BUDGET{END}"
BUDGET_MENU = f"""{MENU_TITLE}
\nPlease select from the following options:
\n1.  Set overall budget
2.  Set budget by category
3.  View budgets
4.  View budget progress
0.  Return to main menu
\nEnter your selection: \
"""
NEW_TERM = """\nPlease select from the following options:
\n1.  Set weekly budget
2.  Set monthly budget
3.  Set annual budget
0.  Cancel set budget
\nEnter your selection: \
"""
W_M_Y = """\nPlease select from the following options:
1.  View this week
2.  View this month
3.  View this year
0.  Cancel
\nEnter your selection: \
"""
COLUMNS_BUDGET = f"""\n{"\033[1m_\033[0m" * 50}\033[1m\n\nCategory\tTerm\t\t\
Amount\n{"\033[1m_\033[0m" * 50}\
"""
INVALID_INPUT = "\nYou entered an invalid input.  Please try again."
SEL_ = f"{cf.SEL_}"
END_ = f"{cf.END_}"
SELECT_1 = f"{SEL_}Set Budget{END_}"
SELECT_2 = f"{SEL_}Set Budget by Category{END_}"
SELECT_3 = f"{SEL_}View Budgets{END_}"
SELECT_4 = f"{SEL_}View Budget Progress{END_}"
OVERSPENT = "\033[91m\U000026a0\033[0m"
OVERALL_PRINT = "_" * 50
PRINT_LINE = "\033[90m_\033[0m" * 50
VIEW_BUDGET = "\n{}\t{}\t\t{}\n" + PRINT_LINE
VIEW_BUDGET_L = "\n{}\t\t{}\t\t{}\n" + PRINT_LINE


class Budget:
    """This class represents a budget

    Attributes
    ----------
    amount : float
        budget amount
    term : str
        'weekly', 'monthly' or 'annual'

    Methods
    ----------
    get_all_att:
        returns attributes of Budget object
    """

    def __init__(self, category, term, amount):
        """Constructs attributes for a budget."""
        self.category = category
        self.term = term
        self.amount = amount

    def __str__(self):
        """Constructs a string in readable format."""
        self.amount = cf.money_format(self.amount)

        # Adjust tabs according to string length so columns are aligned
        # on printing expenses.
        exp_print = VIEW_BUDGET.format(*self.get_all_att())

        if len(self.category) <= 7:
            exp_print = VIEW_BUDGET_L.format(*self.get_all_att())

        return exp_print

    def get_all_att(self):
        """This method returns the attributes of a Budget object.

        :param self: Budget object
        :return: Tuple containing Budget attributes
        """
        return (self.category, self.term, self.amount)


def set_budget_by_category():
    """This function sets a budget for a selected category

    :return: None
    """
    # Get category id number and budget term
    c_id = cf.select_category("categories")
    c = database_commands.get_category_from_id(c_id, "categories")
    print()
    term = cf.get_term(NEW_TERM)

    # Get an amount from user and enter budget into table
    if term:
        new_amount = cf.get_amount()
        database_commands.enter_budget(c_id, new_amount, term)
        cf.clear()
        print(f"\nBudget has been updated for {c} \U00002705\n")


def set_budget():
    """This function gets a term and an amount for a new budget from
    the user and calls function to update tables

    :return: None
    """
    term = cf.get_term(NEW_TERM)

    if term:
        amount = cf.get_amount()
        amount = float(amount)
        update_overall_budgets(term, amount)


def update_overall_budgets(term, amount):
    """This function updates the values in the budget table for a new
    budget

    :param term: 'weekly', 'monthly', or 'annual'
    :param amount: budget amount
    :return: None
    """
    existing_gross = get_existing_gross()

    # Get annual amount from term
    if term == "weekly":
        new_annual_budg = calculations.annual_from_weekly(amount)
    elif term == "monthly":
        new_annual_budg = calculations.annual_from_monthly(amount)
    else:
        new_annual_budg = amount

    # Calculate weekly and monthly budgets and net income from new
    # annual budget
    new_week_budg = calculations.get_week_from_year(new_annual_budg)
    new_month_budg = calculations.get_month_from_year(new_annual_budg)
    new_net_inc = calculations.difference(new_annual_budg, existing_gross)

    # Update table with new budget amounts
    database_commands.enter_goal("budget", new_annual_budg, "annual")
    database_commands.enter_goal("budget", new_week_budg, "weekly")
    database_commands.enter_goal("budget", new_month_budg, "monthly")

    # Update table with gross and net income amounts
    if new_net_inc >= 0:
        database_commands.enter_goal("net income", new_net_inc, "annual")

    # Net income goal cannot be negative. Adjust gross income goal.
    else:
        database_commands.enter_goal("net income", 0, "annual")
        database_commands.enter_goal("gross income", new_annual_budg, "annual")

    amount = cf.money_format(amount)
    cf.clear()
    print("\nIncome and budget goals have been adjusted \U00002705\n")


def get_existing_gross():
    """This function gets the current values set for gross income goal

    :return: existing amounts for gross income
    :rtype: float
    """
    goals_list = database_commands.get_row_list("goals")

    for row in goals_list:
        if row[1] == "gross income":
            existing_gross = row[2]
            return existing_gross
    return None


def get_budgets():
    """This function gets a list of budgets from the budget table

    :return: list of budgets
    :rtype: list of tuples
    """
    rows_list = database_commands.get_row_list("budget")
    budget_list = []

    for row in rows_list:
        cat = database_commands.get_category_from_budget(row[0])
        budget = (cat, row[2], row[1])
        budget_list.append(budget)

    return budget_list


def get_budgets_by_term(term):
    """This function gets a list of budgets in a term

    :param term: 'weekly', 'monthly' or 'annual'
    :return: list of budgets in term
    :rtype: list of tuples
    """
    budget_list = get_budgets()
    budgets_in_term = []

    for budget in budget_list:
        if budget[1] == term:
            budgets_in_term.append(budget)

    return budgets_in_term


def print_budgets(list_of_budgets):
    """This function prints a list of budgets

    :param list_of_budgets: list of rows from budget table
    :return: None
    """
    print(COLUMNS_BUDGET)

    for budget in list_of_budgets:
        if budget[0]:
            budget = Budget(*budget)
            print(budget)


def get_expenses_by_date(term):
    """This function gets a list of rows from expenses table which
    match each day in a list of days

    :param term: 'weekly', 'monthly' or 'annual'
    :return: list of rows from expenses table
    :rtype: list of tuples
    """
    days_list = df.get_days_list(term)
    rows = database_commands.get_expenses_by_date(days_list)
    return rows


def get_list_expenses_in_dates(term):
    """This function gets a list of Expense objects in a term

    :param term: 'weekly', 'monthly', or 'yearly'
    :return: list of Expense objects
    :rtype: list of objects
    """
    expenses_list = get_expenses_by_date(term)
    amounts = []

    for row in expenses_list:
        row = expenses.get_object(row)
        amounts.append(row.amount)

    return expenses_list


def view_progress_by_term(term):
    """This function prints a budget progress by category in a
    specified term

    :param term: 'weekly', 'monthly' or 'annual'
    :return: None
    """
    progress_list = []
    # Get list of rows from expenses in date range
    expenses_list = get_expenses_by_date(term)
    # Get rows from categories and budget tables joined together
    cat_budget = database_commands.get_joined_rows("categories")

    if cat_budget:
        for row in cat_budget:
            expense_list = []
            # Select rows from category-budget table matching term
            if row[5] == term:

                for expense in expenses_list:

                    # Select rows matching category
                    if expense[4] == row[0]:
                        expense_list.append(float(expense[3]))

                # Get amount, category, total and money remaining in budget
                amount = float(row[4])
                category = row[1]
                total = calculations.total_spending(expense_list)
                remain = calculations.difference(total, amount)

                amount = cf.money_format(amount)
                remain = cf.money_format(remain)
                total = cf.money_format(total)

                progress_list.append((total, amount, category, term, remain))

    print_progress(progress_list)


def overall_progress(term):
    """This function prints overall budget progress in a specified term

    :param term: 'weekly', 'monthly' or 'annual'
    :return: None
    """
    budget_goal = database_commands.get_goal("budget", term)

    if budget_goal:
        expenses_list = get_expenses_by_date(term)

        # Get list of expenses in term
        expense_list = []
        for expense in expenses_list:
            expense_list.append(float(expense[3]))

        total = calculations.total_spending(expense_list)
        remain = calculations.difference(total, budget_goal)

        budget_goal = cf.money_format(budget_goal)
        remain = cf.money_format(remain)
        total = cf.money_format(total)

        print(OVERALL_PRINT)
        return print_overall(budget_goal, total, remain, term)

    print(PRINT_LINE)
    return None


def print_overall(budget_goal, total, remain, term):
    """This function prints overall budget progress for a budget

    :param budget_goal: budget amount
    :param total: total spending
    :param remain: amount of money remaining in budget
    :param term: 'weekly', 'monthly' or 'annual'
    :return: None
    """
    print(f"\n\033[1mTOTAL {term.upper()} GOAL\033[0m")
    print(f"Spent {total} of {term} budget of {budget_goal}.")

    if remain[1] != "-":
        print(f"\033[92m\U00002714\033[0m {remain} remaining.")
        print("\nWell done, you're on track!")
    else:
        print(f"{OVERSPENT} {remain[0] + remain[2:]} overspent")

    print(OVERALL_PRINT)
    sleep(0.5)


def print_progress(progress_list):
    """This function prints budget progress for each progress in a list

    :param progress_list: list of progress for each budget
    :return: None
    """
    if progress_list:
        print(PRINT_LINE)

        for item in progress_list:
            print(f"\n\033[1m{item[2].upper()}\033[0m")
            print(f"Spent {item[0]} of {item[3]} budget of {item[1]}.")

            if item[4][1] != "-":
                print(f"\033[92m\U00002714\033[0m {item[4]} remaining.")
            else:
                print(f"{OVERSPENT} {item[4][0] + item[4][2:]} overspent")
            if item != progress_list[-1]:
                print(PRINT_LINE)
            sleep(0.5)

    else:
        print("\nNo budgets set by category for this term.")
        sleep(0.5)


def view_budgets():
    """This function prints all budgets

    :return: None
    """
    budget_list = get_budgets()
    overall = database_commands.get_row_list("goals")

    for row in overall:
        if row[1] == "budget":
            budget_list.append(("OVERALL", row[3], row[2]))

    if budget_list:
        print_budgets(budget_list)
    else:
        print("\nNo budgets found.")
    sleep(0.5)


def budget_menu():
    """This function gets user choice for the budget menu and calls the
    relevant function according to user's selection

    :return: None
    """
    while True:
        menu = input(BUDGET_MENU).strip().replace(".", "")

        # ****** Set overall budget ******
        if menu == "1":
            cf.clear()
            print(SELECT_1)
            set_budget()

        # ****** Set budget by category ******
        elif menu == "2":
            cf.clear()
            print(SELECT_2)
            set_budget_by_category()

        # ****** View Budgets ******
        elif menu == "3":
            cf.clear()
            print(SELECT_3)
            view_budgets()
            print()

        # ****** View Budget Progress ******
        elif menu == "4":
            cf.clear()
            print(SELECT_4)
            term = cf.get_term(W_M_Y)
            cf.clear()
            view_progress_by_term(term)
            overall_progress(term)
            print()

        # ****** Return to main menu ******
        elif menu == "0":
            cf.clear()
            break

        # ****** Add expense ******
        else:
            print(INVALID_INPUT)
            print()
