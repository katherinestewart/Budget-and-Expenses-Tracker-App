"""This module contains the expenses menu. It gets user choice to add
expense, view expenses by category; over a selected term, manage
categories or return to main menu. It also contains all relevant
functions to get the required returns for each selection.
"""

import time
import datetime
from database import database_commands as dc
from functions import common_functions as cf

CAT_DESCRIBE = "\nEnter new category description: "
CATEGORIES = "categories"
COLUMNS = f"""{"\033[1m_\033[0m" * 70}\033[1m\n\nDate\t\tExpense\t\t\t\
Amount\t\tCategory\033[0m\n{"\033[1m_\033[0m" * 70}\
"""
END_ = f"{cf.END_}"
SEL = "\033[36m\033[1m -------- \033[0m\033[1m"
END = "\033[36m\033[1m --------\033[0m"
MENU_TITLE = f"\U0001f4b8{SEL}EXPENSES{END}"
EXPENSES_MENU = f"""{MENU_TITLE}
\nPlease choose from the following options:
\n1.  Add expense
2.  View expenses
3.  View expenses by category
4.  Manage categories
0.  Return to main menu
\nEnter your selection: \
"""
SEL_ = f"{cf.SEL_}"
SELECT_1 = f"{SEL_}Add Expense{END_}"
SELECT_2 = f"{SEL_}View expenses{END_}"
SELECT_3 = f"{SEL_}View expenses by category{END_}"
SELECT_4 = f"{SEL_}Manage categories{END_}"
CATEGORIES_MENU = f"""{SELECT_4}
\nPlease choose from the following options:
\n1.  View categories
2.  Edit category
3.  Add category
0.  Cancel
\nEnter your selection: \
"""
SEARCH_MORE_EXPENSES = """\nEnter 'r' to return to main menu,
or anything else to continue viewing expenses: """
TABLE = "expenses"
PRINT_LINE = "\033[90m_\033[0m" * 70
VIEW_SHORT = "\n{}\t{}\t\t\t{}\t\t{}\n" + PRINT_LINE
VIEW_SHORT_ = "\n{}\t{}\t\t\t{}\t{}\n" + PRINT_LINE
VIEW_LONG = "\n{}\t{}\t\t{}\t\t{}\n" + PRINT_LINE
VIEW_LONG_ = "\n{}\t{}\t\t{}\t{}\n" + PRINT_LINE
VIEW_LONG_X = "\n{}\t{}\t{}\t\t{}\n" + PRINT_LINE
VIEW_LONG_X_ = "\n{}\t{}\t{}\t{}\n" + PRINT_LINE


class Expense:
    """This class represents an expense.

    Attributes
    ----------
    date : str
        date expense was entered
    expense : str
        description of expense
    amount : float
        amount the expense cost
    category : str
        category of expense

    Methods
    ----------
    get_all_att:
        returns attributes of expense
    enter_new_expense:
        enters new expense into expenses table
    """

    def __init__(self, date, expense, amount, category):
        """Constructs attributes for an expense."""
        self.date = date
        self.expense = expense
        self.amount = amount
        self.category = category

    def __str__(self):
        """Constructs a string in readable format."""
        self.amount = cf.money_format(self.amount)

        # Adjust tabs according to string length so columns are aligned
        # on printing expenses.
        if len(self.expense) > 7:
            exp_print = VIEW_LONG.format(*self.get_all_att())
            if len(self.amount) > 7:
                exp_print = VIEW_LONG_.format(*self.get_all_att())
            if len(self.expense) > 15:
                exp_print = VIEW_LONG_X.format(*self.get_all_att())
                if len(self.amount) > 7:
                    exp_print = VIEW_LONG_X_.format(*self.get_all_att())
        else:
            exp_print = VIEW_SHORT.format(*self.get_all_att())
            if len(self.amount) > 7:
                exp_print = VIEW_SHORT_.format(*self.get_all_att())

        return exp_print

    def get_all_att(self):
        """This method returns the attributes of an Expense object.

        :param self: Expense object
        :return: Tuple containing Expense attributes
        """
        return (self.date, self.expense, self.amount, self.category)

    def insert_expense(self):
        """This method enters a new expense into the 'expenses' table.

        :param self: Expense object
        :return: None
        """
        dc.insert_data(dc.INSERT_EXPENSE, self.get_all_att())


def get_expense_description():
    """This function gets a description of a new expense.

    :return: new expense description
    :rtype: str
    """
    while True:
        new_expense = input("\nEnter expense description: ").strip()

        if cf.description_check(new_expense):
            return new_expense

        print(cf.INVALID_INPUT)


def get_expense():
    """This function gets a new expense from the user.

    :return: today's date, expense, amount and category ID number
    :rtype: tuple
    """
    today = datetime.date.today()
    new_expense = get_expense_description()
    new_amount = cf.get_amount()
    cat_choice_id = cf.select_category("categories")
    exp_obj = Expense(today, new_expense, new_amount, cat_choice_id)

    return exp_obj


def get_object(row):
    """This function gets an Expense object from a row from the
    expenses table.

    :param row: row from expenses table
    :return: Expense object
    :rtype: obj
    """
    expense_object = Expense(row[1], row[2], row[3], row[-2])
    return expense_object


def print_row_list(list_of_rows):
    """This function prints a list of rows from the expenses table

    :param list_of_rows: list of rows from expenses table
    :return: None
    """
    if list_of_rows:
        print(COLUMNS)
        for row in list_of_rows:
            item = get_object(row)
            print(item)
    else:
        print(cf.NO_RESULTS)
    print("\n\n")


def expenses_by_date():
    """This function gets rows from expenses table in a selected date
    range

    :return: rows from expenses table
    :rtype: list of tuples
    """
    date_range = cf.select_date_range()
    rows = cf.get_rows_from_dates(date_range, TABLE)

    return rows


def expenses_by_category():
    """This function prints a list of expenses in a selected category

    :return: None
    """
    cat_choice_id = cf.select_category(CATEGORIES)
    cf.clear()

    expense_rows = expenses_by_date()
    expenses_in_category = []

    # If expense matches category selection, append to new list
    for expense in expense_rows:
        if expense[4] == cat_choice_id:
            expenses_in_category.append(expense)

    cf.clear()
    print_row_list(expenses_in_category)
    time.sleep(0.6)


def get_new_category():
    """This function gets a new category description from the user

    :return: category description
    :rtype: str
    """
    cat = input(CAT_DESCRIBE).strip()

    while not cf.description_check(cat):
        cat = input(CAT_DESCRIBE).strip()

    return cat


def view_categories():
    """This function prints all categories for the user to select from

    :return: None
    """
    category_list = dc.get_row_list(CATEGORIES)
    cf.clear()
    cf.print_categories(category_list)
    time.sleep(0.6)


def categories_menu():
    """This function presents the user with options to manage expense
    categories and calls relevant functions according to user selection

    :return: None
    """
    while True:
        cat_menu = input(CATEGORIES_MENU).strip().replace(".", "")

        # ****** View categories ******
        if cat_menu == "1":
            cf.clear()
            view_categories()

        # ****** Edit category ******
        elif cat_menu == "2":
            cf.clear()
            cat_id = cf.select_category(CATEGORIES)
            cat_update = get_new_category()
            dc.update_category(CATEGORIES, cat_id, cat_update)
            print("\nCategory has been updated \U00002705")
            time.sleep(1)
            cf.clear()

        # ****** Add category ******
        elif cat_menu == "3":
            new_cat = get_new_category()
            dc.enter_category(new_cat, CATEGORIES)
            view_categories()
            print("\nCategory added \U00002705")
            time.sleep(1)
            cf.clear()

        # ****** Return to main menu ******
        elif cat_menu == "0":
            cf.clear()
            break

        else:
            print(cf.INVALID_INPUT)


def add_expense():
    """This function calls functions to insert expense into table and
    prints a message to user.

    :return: None
    """
    new_expense = get_expense()
    new_expense.insert_expense()
    cf.clear()

    print(COLUMNS)
    print(new_expense)
    time.sleep(0.6)
    print("\nExpense has been added \U00002705\n")
    time.sleep(0.6)


def expense_menu():
    """This function manages the user selection from the expense menu
    calls the relevant functions according to the menu selection

    :return: None
    """

    while True:
        menu = input(EXPENSES_MENU).strip().replace(".", "")

        # ****** Add expense ******
        if menu == "1":
            cf.clear()
            print(SELECT_1)
            add_expense()

        # ****** View expenses ******
        elif menu == "2":
            cf.clear()
            print(SELECT_2)
            expenses_list = expenses_by_date()
            cf.clear()
            print_row_list(expenses_list)
            time.sleep(0.6)

        # ****** View expenses by category ******
        elif menu == "3":
            cf.clear()
            print(SELECT_3)
            expenses_by_category()

        # ****** Manage Categories ******
        elif menu == "4":
            cf.clear()
            categories_menu()

        # ****** Return to main menu ******
        elif menu == "0":
            cf.clear()
            break

        else:
            cf.clear()
            print(cf.INVALID_INPUT)
