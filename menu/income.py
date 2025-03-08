"""This module contains the income menu. It gets user choice to add
income, view income, manage income sources; view sources of income,
edit income source, add new income source, or return to main menu. It
also contains all relevant functions to get the required returns for
each selection.
"""

import time
import datetime
from functions import common_functions as cf
from database import database_commands as dc

SOURCES = "sources"
COLUMNS_INCOME = f"""{"\033[1m_\033[0m" * 60}\033[1m\n\nDate\t\tSource\t\t\t\
Amount\n{"\033[1m_\033[0m" * 60}\
"""
SEL = "\033[36m\033[1m -------- \033[0m\033[1m"
END = "\033[36m\033[1m --------\033[0m"
MENU_TITLE = f"\U0001f4b7{SEL}INCOME{END}"
INCOME_MENU = f"""{MENU_TITLE}
\nPlease choose from the following options:
\n1.  Add income
2.  View income
3.  View income by source
4.  Manage income sources
0.  Return to main menu
\nEnter your selection: \
"""
SEL_ = "\U00002714\033[0;34m\033[1m ---------- \033[0m\033[1m"
END_ = "\033[0;34m\033[1m ----------\033[0m"
SELECT_1 = f"{SEL_}Add Income{END_}"
SELECT_2 = f"{SEL_}View Income{END_}"
SELECT_3 = f"{SEL_}View Income by Source{END_}"
SELECT_4 = f"{SEL_}Manage Income Sources{END_}"
SOURCES_MENU = f"""{SELECT_4}
\nPlease choose from the following options:
\n1.  View sources of income
2.  Edit income source
3.  Add new income source
0.  Cancel
\nEnter your selection: \
"""
SEARCH_INCOME = """\nEnter 'r' to return to main menu,
or anything else to continue viewing income by category: """
INVALID_INPUT = "\nYou entered an invalid input.  Please try again."
SRC_DESCRIBE = "\nEnter new income source: "
TABLE = "income"
PRINT_LINE = "\033[90m_\033[0m" * 60
VIEW_INCOME = "\n{}\t{}\t\t\t{}\n" + PRINT_LINE
VIEW_INCOME_L = "\n{}\t{}\t\t{}\n" + PRINT_LINE
VIEW_INCOME_XL = "\n{}\t{}\t{}\n" + PRINT_LINE


class Income:
    """This class represents an income.

    Attributes
    ----------
    date : str
        date income was entered
    source : str
        description of income source
    amount : float
        amount of income

    Methods
    ----------
    get_all_att:
        returns attributes of Income object
    insert_income:
        inserts new income into Income table
    """

    table = "income"

    def __init__(self, date, source, amount):
        """Constructs attributes for an income."""
        self.date = date
        self.source = source
        self.amount = amount

    def __str__(self):
        """Constructs a string in readable format."""
        self.amount = cf.money_format(self.amount)
        self.source = str(self.source)

        # Adjust tabs according to string length so columns are aligned
        # on printing expenses.
        exp_print = VIEW_INCOME.format(*self.get_all_att())
        if len(self.source) > 7:
            exp_print = VIEW_INCOME_L.format(*self.get_all_att())
        if len(self.source) > 15:
            exp_print = VIEW_INCOME_XL.format(*self.get_all_att())
        return exp_print

    def get_all_att(self):
        """This method returns the attributes of an Income object.

        :param self: Income object
        :return: Tuple containing Income attributes
        """
        return (self.date, self.source, self.amount)

    def insert_income(self):
        """This method enters a new income into the 'income' table.

        :param self: Income object
        :return: None
        """
        dc.insert_data(dc.INSERT_INCOME, self.get_all_att())


def get_income():
    """This function gets a new income from the user.

    :return: today's date, income source and amount
    :rtype: tuple
    """
    today = datetime.date.today()
    id_choice = cf.select_category("sources")
    new_amount = cf.get_amount()

    inc_object = Income(today, id_choice, new_amount)

    return inc_object


def get_object(row):
    """This function gets an Income object from its row in income table

    :param row: row in income table
    :return: Income object
    :rtype: object
    """
    income_object = Income(row[1], row[-1], row[3])
    return income_object


def print_row_list(list_of_rows):
    """This function prints a list of rows from the income table

    :param list_of_rows: list of rows from income table
    :return: None
    """
    if list_of_rows:
        print(COLUMNS_INCOME)
        for row in list_of_rows:
            item = get_object(row)
            print(item)
    else:
        print(cf.NO_RESULTS)


def income_by_date():
    """This function selects rows from the income table matching a
    specified date range

    :return: list of rows from income table
    :rtype: list of tuples
    """
    date_range = cf.select_date_range()
    rows = cf.get_rows_from_dates(date_range, TABLE)

    return rows


def income_by_source():
    """This function prints a list of incomes from a selected income
    source

    :return: None
    """
    source_choice_id = cf.select_category(SOURCES)
    income_rows = income_by_date()
    income_from_source = []

    # If income matches source selection, append to new list
    for income in income_rows:
        if income[2] == int(source_choice_id):
            income_from_source.append(income)

    cf.clear()
    print_row_list(income_from_source)
    print("\n\n")


def get_new_source():
    """This function gets a new income source from the user

    :return: income source description
    :rtype: str
    """
    while True:
        src = input(SRC_DESCRIBE).strip()

        if cf.description_check(src):
            return src

        print(INVALID_INPUT)


def view_sources():
    """This function prints income sources for the user to select from

    :return: None
    """
    source_list = dc.get_row_list(SOURCES)
    cf.print_categories(source_list)


def sources_menu():
    """This function manages user selection for income sources and
    calls relevant functions according to this selection

    :return: None
    """
    while True:
        src_menu = input(SOURCES_MENU).strip().replace(".", "")

        # ****** View sources of income ******
        if src_menu == "1":
            cf.clear()
            view_sources()
            print()

        # ****** Edit income source ******
        elif src_menu == "2":
            cf.clear()
            src_id = cf.select_category(SOURCES)
            src_update = get_new_source()
            dc.update_category(SOURCES, src_id, src_update)
            view_sources()
            print("\nIncome source has been updated \U00002705\n")

        # ****** Add new income source ******
        elif src_menu == "3":
            cf.clear()
            new_cat = get_new_source()
            dc.enter_category(new_cat, SOURCES)
            view_sources()
            print("\nIncome source added \U00002705\n")

        # ****** Cancel ******
        elif src_menu == "0":
            cf.clear()
            break

        else:
            print(cf.INVALID_INPUT)
    cf.clear()


def income_menu():
    """This function gets user input for the income menu and calls
    relevant functions according to this selection

    :return: None
    """
    while True:
        menu = input(INCOME_MENU).strip().replace(".", "")
        # ****** Add income ******
        if menu == "1":
            cf.clear()
            print(SELECT_1)

            # Get income object
            new_income = get_income()

            new_income.insert_income()
            cf.clear()
            print(COLUMNS_INCOME)
            n = new_income
            n.source = dc.get_category_from_id(n.source, "sources")
            print(new_income)
            print("\nIncome has been added \U00002705\n\n")
            time.sleep(0.6)

        # ****** View income ******
        elif menu == "2":
            cf.clear()
            print(SELECT_2)
            income_list = income_by_date()

            cf.clear()
            print_row_list(income_list)
            print("\n\n")

        # ****** View income by source ******
        elif menu == "3":
            cf.clear()
            print(SELECT_3)
            income_by_source()

        # ****** Manage income sources ******
        elif menu == "4":
            cf.clear()
            sources_menu()

        # ****** Return to main menu ******
        elif menu == "0":
            cf.clear()
            break

        # ****** Add expense ******
        else:
            cf.clear()
            print(INVALID_INPUT)
