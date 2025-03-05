"""This module contains functions with logic which is commonly used
across multiple modules: expenses.py, income.py, budget.py and goals.py.
"""

import os
import datetime
from database import database_commands

SEL_DATES = """\n\U0001f5d3  Please choose from the following time periods:\n
1.  This month
2.  3 months
3.  6 months
4.  Past year
5.  All history
0.  Exit
\nEnter your selection: \
"""
INVALID_INPUT = "You entered an invalid input.  Please try again.\n"
NO_RESULTS = "\nNo results found for your search."
SEL_ = "\n\U00002714\033[0;34m\033[1m --- \033[0m\033[1m"
END_ = "\033[0;34m\033[1m ---\033[0m"
SELECT_1 = f"{SEL_}Set Budget{END_}"
SELECT_2 = f"{SEL_}Set Budget by Category{END_}"


def clear():
    os.system('cls||clear')


def get_term(string):
    """This function returns a term from a user choice

    :param string: '1', '2', '3' or '0'
    :return: 'weekly', 'monthly', 'annual' or None
    :rtype: str or None
    """
    term_dict = {
        "1": "weekly",
        "2": "monthly",
        "3": "annual",
    }

    while True:
        new_term = input(string).strip().replace(".", "")
        if new_term in term_dict:
            return term_dict[new_term]
        if new_term == "0":
            break
        print(INVALID_INPUT)

    return None


def select_date_range():
    """This function gets a date range selection from user

    :return: '1', '2', '3', '4', '5', or '0'
    :rtype: str
    """
    date_range = input(SEL_DATES).strip().replace(".", "")

    while date_range not in ("1", "2", "3", "4", "5", "0"):
        date_range = input(SEL_DATES).strip().replace(".", "")

    return date_range


def money_format(some_amount):
    """This function convert an amount of money into a string with £
    sign and 2 decimal places.

    :return: amount with £ and 2 dp
    :rtype: str
    """
    if len(str(some_amount)) == 1:
        some_amount = str(some_amount) + ".00"
    if str(some_amount)[-1] == ".":
        some_amount = str(some_amount) + "00"
    if len(str(some_amount)) > 1:
        if str(some_amount)[-2] == ".":
            some_amount = str(some_amount) + "0"

    some_amount = "£" + str(some_amount)
    return some_amount


def get_rows_from_dates(date_range, table):
    """This function selects rows from a table which match the date
    range selected by user.

    :param date_range: User selection: '1', '2', '3', '4' or '5'
    :param table: str table name in database
    :return: rows from table which match date range
    :rtype: list of tuples
    """
    today = datetime.date.today()
    # Selection "1" is today's month.
    year_month = str(today)[:7]  # Get YYYY-MM from YYYY-MM-DD

    # Get rows for this month
    rows_in_months = database_commands.get_rows(year_month, table)

    # "2" selects 3 months, "3" selects 6 months, "4" selects past year
    if date_range in ("2", "3", "4"):

        time_period = get_range_for_search(date_range)

        # List of items in format YYYY-MM from date range selected
        months_list = select_months(time_period)

        # Get rows for each previous month
        for year_month in months_list:
            add_months = database_commands.get_rows(year_month, table)

            # Append rows to list for each month
            for row in add_months:
                rows_in_months.append(row)

    # Get rows for all time
    if date_range == "5":
        rows_in_months = database_commands.get_joined_rows(table)

    return rows_in_months


def select_months(time_period):
    """This function gets the month and year in the format YYYY-MM for
    each month in the specified time period.

    :param time_period: integer range
    :return: previous months in specified range
    :rtype: list
    """
    today = datetime.date.today()
    current_month = today.replace(day=1)  # Get first day of today's month
    months_list = []

    for _ in time_period:
        first = current_month.replace(day=1)  # Get first day of current month
        # Rewind one day to move to previous month
        current_month = first - datetime.timedelta(days=1)  # [1]
        # Append previous month to months_list
        months_list.append(current_month.strftime("%Y-%m"))

    return months_list


def get_range_for_search(selection):
    """This function gets a range of values user selection for a number
    of months to search

    :param selection: '2', '3' or '4'
    :return: range to search
    :rtype: range
    """
    if selection == "2":
        num_months = range(2)
    elif selection == "3":
        num_months = range(5)
    else:
        num_months = range(11)

    return num_months


def select_category(table):
    """This function gets an id number from a table from its
    description.

    :param table: str table name in database
    :return: id number
    :rtype: int
    """
    category_list = database_commands.get_row_list(table)
    print_categories(category_list)

    # dict keys: user selection, values: category id number
    category_dict = get_category_dict(category_list)

    # Get user selection
    category_select = input("\nEnter selection: ")

    while category_select not in category_dict:
        print(INVALID_INPUT)
        category_select = input("\nEnter selection: ")

    # Get category id number
    category_choice = int(category_dict.get(category_select))

    return category_choice


def get_category_dict(category_list):
    """This function prints the existing categories for the user and
    returns a dictionary of number of category printed to user as
    values and the category primary key in 'categories' table as
    values.

    :return: dictionary to get category id number
    :rtype: dict
    """
    category_dict = {}

    for i, category in enumerate(category_list):
        category_dict[str(i + 1)] = str(category[0])

    return category_dict


def print_categories(category_list):
    """This function prints expense categories or income sources

    :param category_list: list of categories
    :return: None
    """
    print("\n\U0001f9fe \033[1mCategories: \033[0m\n")

    for i, category in enumerate(category_list):
        if i + 1 < 10:
            print(f"{i+1}.  {category[1]}")
        else:
            print(f"{i+1}. {category[1]}")


def get_amount():
    """This function gets an amount from the user

    :return: new amount
    :rtype: str
    """
    while True:
        new_amount = input("\nEnter amount: ").strip()

        if amount_check(new_amount):
            return new_amount

        print(INVALID_INPUT)


def amount_check(new_amount):
    """This function checks that a user input is valid for a monetary
    amount.

    :param new_amount: amount entered by user
    :return: True if valid or False if invalid
    :rtype: bool
    """
    try:
        amount = float(new_amount)
        pounds, pence = str(amount).split(".")
        if len(pence) <= 2 and pounds[0] != "-":
            return True
        return False
    except ValueError:
        return False


def description_check(new_expense):
    """Checks validity of user input for a description for an expense
    or income.

    :param new_expense: str description
    :return: True if valid or False if invalid
    :rtype: bool
    """
    if new_expense == "":
        print("You didn't enter anything.")
        return False
    if len(new_expense) > 22:
        print("You entered too many characters.")
        return False

    return True
