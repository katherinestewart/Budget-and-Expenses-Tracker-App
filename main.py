"""This module contains the entry point for the Budget and Expenses
Tracker App.
"""

import os
from menu import main_menu

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def main():
    """This function is the main entry point of the programme."""
    main_menu.main_menu()


if __name__ == "__main__":
    main()
