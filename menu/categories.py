"""This module contains the categories menu and all functions and
classes"""

from time import sleep
from functions import common_functions as cf
from database import database_commands as dc

CATEGORIES = "categories"
UPDATE_CATEGORY = """UPDATE categories SET category = ? WHERE id = ?"""
ENTER_DESCRIPTION = "\nEnter new category description: "
SEL_ = f"{cf.SEL_}"
END_ = f"{cf.END_}"
INSERT_CATEGORY = """INSERT INTO categories(category) VALUES(?)"""
SELECT_4 = f"{SEL_}Manage categories{END_}"
CATEGORIES_MENU = f"""{SELECT_4}
\nPlease choose from the following options:
\n1.  View categories
2.  Edit category
3.  Add category
0.  Cancel
\nEnter your selection: \
"""


class Category:
    """This class represents a category.

    Attributes
    ----------
    id: str
        primary key in category table
    description : str
        description of category

    Methods
    ----------
    get_all_att:
        returns attributes of category
    insert_category:
        enters new category into categories table
    budget_id:
        foreign key to join with primary key in budget table
    """

    def __init__(self, id_, description, budget_id):
        """Constructs attributes for a category."""
        self.id_ = id_
        self.description = description
        self.budget_id = budget_id

    def __str__(self):
        """Constructs a string in readable format."""
        return self.description

    def get_all_att(self):
        """This method returns the attributes of a Category object.

        :param self: Expense object
        :return: Tuple containing Expense attributes
        """
        return (self.id_, self.description)

    def insert_category(self):
        """This method enters a new category into the 'categories'
        table.

        :param self: Category object
        :return: None
        """
        dc.insert_data(INSERT_CATEGORY, (self.description,))

    def update_category(self, description_update):
        """This method updates category in categories table with a new
        category description.

        :param self: Category object to be updated
        :param description_update: New description
        :return: None
        """
        dc.insert_data(UPDATE_CATEGORY, (description_update, self.id_))


def get_categories():
    """This function gets a list of all categories in the database as
    objects.

    :return: list of Category objects
    :rtype: list of obj
    """
    category_list = []
    rows = dc.get_row_list(CATEGORIES)

    for row in rows:
        category_list.append(Category(*row))

    return category_list


def print_categories():
    """This function prints a list of categories.

    :return: None
    """
    category_list = get_categories()
    print("\n\U0001f9fe \033[1mCategories: \033[0m\n")

    for i, category in enumerate(category_list):
        if i + 1 < 10:
            print(f"{i+1}.  {category.description}")
        else:
            print(f"{i+1}. {category.description}")


def get_category_description():
    """This function gets a new category description from the user.

    :return: category description
    :rtype: str
    """
    while True:
        description = input(ENTER_DESCRIPTION).strip()

        if cf.description_check(description):
            return description


def select_category():
    """This function gets a category object from user selection.

    :param table: str table name in database
    :return: id number
    :rtype: int
    """
    category_list = get_categories()
    print_categories()

    while True:
        category_select = input("\nEnter selection: ")
        if category_selection_check(category_select, len(category_list)):
            break
        print(cf.INVALID_INPUT)

    category_object = category_list[int(category_select)-1]

    return category_object


def category_selection_check(category_select, number_of_categories):
    """This function checks the user input validity for a category
    selection.

    :param category_select: number choice from printed categories
    :param number_of_categories: number of rows in categories table
    :return: True if valid or False if invalid
    :rtype: bool
    """
    try:
        category_select = int(category_select)
        if 1 <= category_select <= number_of_categories:
            return True
        return False
    except TypeError:
        return False


def edit_category():
    """This function gets an updated category description from the user
    and updates the relevant row in the categories table.

    :return: None
    """
    category_selection = select_category()
    category_update = get_category_description()
    category_selection.update_category(category_update)
    cf.clear()

    print_categories()
    print("\nCategory has been updated \U00002705")
    cf.finish_viewing()


def add_category():
    """This function adds a new category to the database.

    :return: None
    """
    category = Category(None, get_category_description(), None)
    category.insert_category()
    cf.clear()

    print_categories()
    sleep(0.6)
    print("\nCategory added \U00002705")
    cf.finish_viewing()


def categories_menu():
    """This function presents the user with options to manage expense
    categories and calls relevant functions according to user selection

    :return: None
    """
    while True:
        cf.clear()
        cat_menu = input(CATEGORIES_MENU).strip().replace(".", "")

        # ****** View categories ******
        if cat_menu == "1":
            cf.clear()
            print_categories()
            cf.finish_viewing()

        # ****** Edit category ******
        elif cat_menu == "2":
            cf.clear()
            edit_category()

        # ****** Add category ******
        elif cat_menu == "3":
            add_category()

        # ****** Return to main menu ******
        elif cat_menu == "0":
            break

        else:
            print(cf.INVALID_INPUT)
