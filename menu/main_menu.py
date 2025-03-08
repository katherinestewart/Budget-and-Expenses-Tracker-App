"""This module is the main menu. It gets the user choice for expenses,
income, budget, financial goals or to exit the programme.

References
----------
[1] Stack Overflow (for the function display_message)
https://stackoverflow.com/questions/71675811/how-do-i-make-a-delay-in-the-printing-of-each-letter-in-my-code  # noqa
"""

from time import sleep
from database import database_commands as dc
from menu import expenses, income, budget, goals
from functions import common_functions as cf

INVALID_INPUT = "\nYou entered an invalid input.  Please try again."
MAIN_MENU = """\U0001f3e0 \033[1m\033[96m============ \033[0m\033[1m\
MAIN MENU\033[36m ============\033[0m\033[0m
\nPlease choose from the following options:
\n1.  Expenses
2.  Income
3.  Budget
4.  Financial Goals
0.  Quit
\nEnter your selection: \
"""
WELCOME = "Welcome to the Expenses and Budget Tracker App! \U0001f4b0"


def main_menu():
    """Gets the user selection from the main menu and calls relevant
    module from selection

    :return: None
    """
    dc.create_tables()

    display_message(WELCOME)

    # ********* Menu Selection *********
    while True:
        menu = input(MAIN_MENU).strip().replace(".", "")

        # ****** Expenses ******
        if menu == "1":
            cf.clear()
            expenses.expense_menu()

        # ****** Income ******
        elif menu == "2":
            cf.clear()
            income.income_menu()

        # ****** Budget ******
        elif menu == "3":
            cf.clear()
            budget.budget_menu()

        # ****** Financial Goals ******
        elif menu == "4":
            cf.clear()
            goals.goals_menu()

        # ****** Exit ******
        elif menu == "0":
            cf.clear()
            display_message("\nSee you next time! \U0001f44b\n")

            # Final break point to close the programme naturally
            break

        else:
            print(INVALID_INPUT)


def display_message(message):
    """This function displays welcome and goodbye messages with a time
    delay

    :param message: welcome or goodbye message for user
    :return: None
    """
    x = ""
    for char in message:
        x += char
        print(x)
        sleep(0.04)
        cf.clear()
