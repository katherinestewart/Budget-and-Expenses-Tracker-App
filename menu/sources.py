"""This module contains all functions and classes for income sources.
"""

from time import sleep
from functions import common_functions as cf
from database import database_commands as dc

SOURCES = "sources"
UPDATE_SOURCE= """UPDATE sources SET source = ? WHERE id = ?"""
INSERT_SOURCE = """INSERT INTO sources(source) VALUES(?)"""
SOURCES = "sources"
ENTER_DESCRIPTION = "\nEnter new income source description: "
SEL_ = "\U00002714\033[0;34m\033[1m ---------- \033[0m\033[1m"
END_ = "\033[0;34m\033[1m ----------\033[0m"
SELECT_4 = f"{SEL_}Manage Income Sources{END_}"
SOURCES_MENU = f"""{SELECT_4}
\nPlease choose from the following options:
\n1.  View sources of income
2.  Edit income source
3.  Add new income source
0.  Cancel
\nEnter your selection: \
"""


class Source:
    """This class represents a source of income.

    Attributes
    ----------
    id: str
        primary key in sources table
    description : str
        description of income source

    Methods
    ----------
    get_all_att:
        returns attributes of income source
    insert_source:
        enters new income source into sources table
    """

    def __init__(self, id_, description):
        """Constructs attributes for a category."""
        self.id_ = id_
        self.description = description

    def __str__(self):
        """Constructs a string in readable format."""
        return self.description

    def get_all_att(self):
        """This method returns the attributes of a Source object.

        :param self: Source object
        :return: Tuple containing Source attributes
        """
        return (self.id_, self.description)

    def insert_source(self):
        """This method enters a new category into the 'categories'
        table.

        :param self: Category object
        :return: None
        """
        dc.insert_data(INSERT_SOURCE, (self.description,))

    def update_source(self, description_update):
        """This method updates category in categories table with a new
        category description.

        :param self: Category object to be updated
        :param description_update: New description
        :return: None
        """
        dc.insert_data(UPDATE_SOURCE, (description_update, self.id_))


def get_sources():
    """This function gets a list of all sources in the database as
    objects.

    :return: list of Source objects
    :rtype: list of obj
    """
    category_list = []
    rows = dc.get_row_list(SOURCES)

    for row in rows:
        category_list.append(Source(*row))

    return category_list


def print_sources():
    """This function prints a list of sources.

    :return: None
    """
    source_list = get_sources()
    print("\n\U0001f9fe \033[1mIncome Sources: \033[0m\n")

    for i, source in enumerate(source_list):
        if i + 1 < 10:
            print(f"{i+1}.  {source.description}")
        else:
            print(f"{i+1}. {source.description}")


def get_source_description():
    """This function gets a new income source description from the
    user.

    :return: source description
    :rtype: str
    """
    while True:
        description = input(ENTER_DESCRIPTION).strip()

        if cf.description_check(description):
            return description


def select_source():
    """This function gets a income source object from user selection.

    :param table: str table name in database
    :return: id number
    :rtype: int
    """
    source_list = get_sources()
    print_sources()

    while True:
        source_select = input("\nEnter selection: ")
        if source_selection_check(source_select, len(source_list)):
            break
        print(cf.INVALID_INPUT)

    source_object = source_list[int(source_select)-1]

    return source_object


def source_selection_check(source_select, number_of_sources):
    """This function checks the user input validity for a source
    selection.

    :param source_select: number choice from printed sources
    :param number_of_sources: number of rows in sources table
    :return: True if valid or False if invalid
    :rtype: bool
    """
    try:
        source_select = int(source_select)
        if 1 <= source_select <= number_of_sources:
            return True
        return False
    except TypeError:
        return False


def edit_source():
    """This function gets an updated source description from the user
    and updates the relevant row in the sources table.

    :return: None
    """
    source_selection = select_source()
    source_update = get_source_description()
    source_selection.update_source(source_update)
    cf.clear()

    print_sources()
    print("\nIncome source has been updated \U00002705")
    cf.finish_viewing()


def add_source():
    """This function adds a new income source to the database.

    :return: None
    """
    source = Source(None, get_source_description())
    source.insert_source()
    cf.clear()

    print_sources()
    sleep(0.6)
    print("\nIncome source added \U00002705")
    cf.finish_viewing()


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
            print_sources()
            cf.finish_viewing()
            cf.clear()

        # ****** Edit income source ******
        elif src_menu == "2":
            cf.clear()
            edit_source()
            cf.clear()

        # ****** Add new income source ******
        elif src_menu == "3":
            add_source()
            cf.clear()

        # ****** Cancel ******
        elif src_menu == "0":
            cf.clear()
            break

        else:
            print(cf.INVALID_INPUT)
    cf.clear()
