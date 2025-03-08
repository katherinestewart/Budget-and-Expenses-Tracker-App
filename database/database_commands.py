"""This module contains all functions with logic to interact with the
database finances.db. This is the only module which accesses the
database. There are six tables; expenses, income, categories, sources,
budget and goals.
"""

from contextlib import contextmanager
import sqlite3
from database import populate_finances_db as pf


CREATE_EXPENSES_TABLE = """CREATE TABLE IF NOT EXISTS expenses
(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, expense TEXT,
amount FLOAT, categoryID INTEGER, FOREIGN KEY(categoryID)
REFERENCES categories(id))"""
CREATE_INCOME_TABLE = """CREATE TABLE IF NOT EXISTS income
(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, sourceID INT,
amount FLOAT, FOREIGN KEY(sourceID) REFERENCES income_sources(id))"""
CREATE_CATEGORY_TABLE = """CREATE TABLE IF NOT EXISTS categories
(id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, budgetID TEXT,
FOREIGN KEY(budgetID) REFERENCES budget(id))"""
CREATE_BUDGET_TABLE = """CREATE TABLE IF NOT EXISTS budget
(id INTEGER PRIMARY KEY AUTOINCREMENT, amount FLOAT, term TEXT)"""
CREATE_GOALS_TABLE = """CREATE TABLE IF NOT EXISTS goals
(id INTEGER PRIMARY KEY AUTOINCREMENT, goal TEXT, amount FLOAT, term TEXT)"""
CREATE_SOURCES_TABLE = """CREATE TABLE IF NOT EXISTS sources
(id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT)"""
MAX_BUDGET_ID = """SELECT MAX(id) FROM budget"""
INSERT_EXPENSE = """INSERT INTO expenses(date, expense, amount, categoryID)
VALUES(?,?,?,?)"""
INSERT_INCOME = """INSERT INTO income(date, sourceID, amount) VALUES(?,?,?)"""
INSERT_CATEGORY = """INSERT INTO categories(category) VALUES(?)"""
INSERT_BUDGET = """INSERT INTO budget(amount, term) VALUES(?,?)"""
INSERT_GOAL = """INSERT INTO goals(goal, amount, term) VALUES(?,?,?)"""
INSERT_SOURCE = """INSERT INTO sources(source) VALUES(?)"""
UPDATE_CATEGORY = """UPDATE categories SET budgetID = ? WHERE id = ?"""
LAST_INSERTED_ID = """SELECT last_insert_rowid()"""

SELECT_CATEGORIES = """SELECT * FROM categories INNER JOIN budget ON
categories.budgetID=budget.id"""
SELECT_EXPENSES = """SELECT * FROM expenses INNER JOIN categories ON
expenses.categoryID=categories.id ORDER BY id DESC"""
SELECT_INCOME = """SELECT * FROM income INNER JOIN sources ON
income.sourceID=sources.id ORDER BY id DESC"""
CAT_UPDATE = """UPDATE categories SET category = ? WHERE id = ?"""
DELETE_BUDGET = """DELETE FROM budget WHERE id = ?"""
DEL_GOAL = """DELETE FROM goals WHERE id = ?"""
DELETE_GOAL = """DELETE FROM goals WHERE goal = ? AND term = ?"""
ENTER_CAT = """INSERT INTO categories(category) VALUES(?)"""
ENTER_SRC = """INSERT INTO sources(source) VALUES(?)"""
MAX_BUDGET_ID = """SELECT MAX(id) FROM budget"""
SEL_CAT_FROM_BUDG = """SELECT category FROM categories WHERE budgetID = ?"""
SELECT_DATE_AMOUNT = """SELECT date, amount FROM expenses WHERE catID = ?"""
SELECT_GOAL = """SELECT * FROM goals WHERE goal = ? AND term = ?"""
SELECT_ROWS = """SELECT * FROM {}"""
SELECT_EXPS_BY_DATE = """SELECT * FROM expenses WHERE date = ?"""
SELECT_INC_BY_DATE = """SELECT * FROM income WHERE date = ?"""
SELECT_CATEGORY = """SELECT category FROM categories WHERE id = ?"""
SELECT_INC_CAT = """SELECT source FROM sources WHERE id = ?"""
SRC_UPDATE = """UPDATE sources SET source = ? WHERE id = ?"""
TABLE_EXISTS = """SELECT name FROM sqlite_master WHERE type='table'"""
UPDATE_CAT_BUDGET = """UPDATE categories SET budgetID = ? WHERE id = ?"""
SELECT_FIRST_EXPENSE = """SELECT * FROM expenses WHERE id = 1"""


@contextmanager
def get_cursor():
    """This function catches any errors when connecting to the database
    and creates a cursor.

    :return: cursor
    :rtype: cursor
    """
    try:
        db = sqlite3.connect("finances.db")
        cursor = db.cursor()
        yield cursor
    except sqlite3.Error as e:
        db.rollback()
        raise e
    else:
        db.commit()
    finally:
        db.close()


def insert_data(string, args):
    """This function inserts data into the database.

    :param string: SQLite command
    :param args: tuple with arguments for command
    :return: None
    """
    with get_cursor() as cursor:
        cursor.execute(string, args)


def insert_many(command):
    """This function inserts a list of data into the database.

    :param command: tuple containing (str, list)
    :return: None
    """
    with get_cursor() as cursor:
        cursor.executemany(*command)


def fetch_one(command):
    """This function fetches data from one row in the database.

    :param input: SQLite command
    :param args: arguments for SQLite command
    :return: data from one row
    :rtype: tuple
    """
    with get_cursor() as cursor:
        cursor.execute(command)
        data = cursor.fetchone()

    return data


def fetch_one_with_args(string, args):
    """This function fetches data from one row in the database by
    selected arguments.

    :param input: SQLite command
    :param args: arguments for SQLite command
    :return: data from one row
    :rtype: tuple
    """
    with get_cursor() as cursor:
        cursor.execute(string, args)
        data = cursor.fetchone()

    return data


def fetch_all(command):
    """This function fetches data from one or more rows in the
    database.

    :param input: SQLite command
    :param args: arguments for SQLite command
    :return: data from one or more rows
    :rtype: List of tuples
    """
    with get_cursor() as cursor:
        cursor.execute(command)
        data = cursor.fetchall()

    return data


def fetch_all_with_args(string, args):
    """This function fetches data from one or more rows in the
    database which match selected arguments.

    :param input: SQLite command
    :param args: arguments for SQLite command
    :return: data from one or more rows
    :rtype: List of tuples
    """
    with get_cursor() as cursor:
        cursor.execute(string, args)
        data = cursor.fetchall()

    return data


def create_tables():
    """This function creates all tables in the database if they don't
    exist and calls function to populate tables.

    :return: None
    """
    commands = [
        CREATE_EXPENSES_TABLE,
        CREATE_CATEGORY_TABLE,
        CREATE_INCOME_TABLE,
        CREATE_SOURCES_TABLE,
        CREATE_BUDGET_TABLE,
        CREATE_GOALS_TABLE,
    ]

    for command in commands:
        with get_cursor() as cursor:
            cursor.execute(command)

    populate_tables()


def populate_tables():
    """This function checks if there is any data in the expenses table
    and if not it populates all tables with dummy data for testing.

    :return: None
    """
    if not fetch_one(SELECT_FIRST_EXPENSE):
        pf.populate_tables()


def insert_budget(category_id, budget):
    """This function enters a new budget assigned to a category.

    :param category_id: primary key in categories table
    :param budget: tuple containing (amount, term)
    :return: None
    """
    insert_data(INSERT_BUDGET, budget)
    budget_id = fetch_one(MAX_BUDGET_ID)
    insert_data(UPDATE_CATEGORY, (*budget_id, category_id))


def enter_category(new_cat, table):
    """This function enters a new category in a table.

    :param new_cat: new expense category or income source
    :param table: expenses or sources table in database
    :return: None
    """

    if table == "categories":
        insert_data(ENTER_CAT, (new_cat,))
    else:
        insert_data(ENTER_SRC, (new_cat,))


def get_row_list(table):
    """This function gets a list of all the rows in a table.

    :param table: table in database
    :return: all rows
    :rtype: list
    """
    rows = fetch_all(SELECT_ROWS.format(table))
    return rows


def get_rows(year_month, table):
    """This function gets all rows from a table and appends rows to a
    list where the date they were entered matches a selected month.

    :param year_month: YYYY-MM
    :return: all rows which match year_month from table
    :rtype: list of tuples
    """
    rows_list = []
    rows = get_joined_rows(table)

    for row in rows:
        if row[1][:7] == year_month:
            rows_list.append(row)

    return rows_list


def get_joined_rows(table):
    """This function gets all rows from a joined table.

    :param table: table name
    :return: all rows from joined table
    :rtype: list of tuples
    """
    table_dict = {
        "expenses": SELECT_EXPENSES,
        "income": SELECT_INCOME,
        "categories": SELECT_CATEGORIES,
    }

    rows_list = fetch_all(table_dict[table])

    return rows_list


def get_category_from_id(id_, table):
    """This function gets the description of an expenses category or
    income source from its id number

    :param category_id: primary key in table
    :param table: 'categories' or 'sources'
    :return: category
    :rtype: str
    """
    table_dict = {"categories": SELECT_CATEGORY, "sources": SELECT_INC_CAT}

    category = fetch_one_with_args(table_dict[table], (id_,))
    return category[0]


def get_category_from_budget(budget_id):
    """This function gets the category description, for a budget set by
    category, from its budget id number

    :param budget_id: budget primary key which is category foreign key
    :return: category description or None
    :rtype: str or None
    """
    category = fetch_one_with_args(SEL_CAT_FROM_BUDG, (budget_id,))

    if category:
        return category[0]

    return None


def update_category(table, id_, update):
    """This function updates a description for an expense category or
    an income source.

    :param table: 'categories' or 'sources'
    :param cat_id: primary key id number
    :return: None
    """
    table_dict = {
        "categories": CAT_UPDATE,
        "sources": SRC_UPDATE,
    }
    insert_data(table_dict[table], (update, id_))


def enter_budget(category_id, amount, term):
    """This function enters a new budget assigned to a category

    :param category_id: primary key in categories table
    :param amount: new budget amount
    :param term: "weekly", "monthly", or "annual"
    :return: None
    """
    cat_rows = get_row_list("categories")

    for row in cat_rows:
        if row[0] == category_id:
            insert_data(DELETE_BUDGET, (row[2],))

    insert_data(INSERT_BUDGET, (amount, term))
    budget_id = fetch_one(MAX_BUDGET_ID)
    insert_data(UPDATE_CAT_BUDGET, (*budget_id, category_id))


def get_expenses_date_amount(category_id):
    """This function gets the date and amount of expenses from a chosen
    category.

    :param category_id: foreign key in expenses table
    :return: date and amount of expenses
    :rtype: list of tuples
    """
    date_amount = fetch_one_with_args(SELECT_DATE_AMOUNT, (category_id,))

    return date_amount


def get_expenses_by_date(days_list):
    """This function gets expenses for each day in a list.

    :param days_list: list of dates
    :return: list of rows from expenses table
    :rtype: list of tuples
    """
    expenses_list = []

    for day in days_list:
        rows = fetch_all_with_args(SELECT_EXPS_BY_DATE, (day,))
        for row in rows:
            expenses_list.append(row)

    return expenses_list


def get_income_by_date(days_list):
    """This function gets income for each day in a list

    :param days_list: list of days
    :return: list of rows from income table
    :rtype: list of tuples
    """
    income_list = []

    for day in days_list:
        rows = fetch_all_with_args(SELECT_INC_BY_DATE, (day,))
        if rows:
            for row in rows:
                income_list.append(row)

    return income_list


def enter_goal(goal, amount, term):
    """This function enters a new goal into the goals table

    :param goal: 'budget', 'net income' or 'gross income'
    :param amount: amount of money in goal
    :param term: 'weekly', 'monthly' or 'annual'
    :return: None
    """
    if goal in ("net income", "gross income"):
        goals_list = get_row_list("goals")
        for row in goals_list:

            # Delete goal if one already exists
            if row[1] == goal:
                insert_data(DEL_GOAL, (row[0],))

    # Delete goal if one already exists
    if goal == "budget":
        insert_data(DELETE_GOAL, (goal, term))

    insert_data(INSERT_GOAL, (goal, amount, term))


def get_goal(goal, term):
    """This function gets a goal amount from the goals table from its
    description and term

    :param goal: 'budget', 'net income' or 'gross income'
    :param term: 'weekly', 'monthly' or 'annual'
    :return: goal amount or None
    :rtype: float or None
    """
    row = fetch_one_with_args(SELECT_GOAL, (goal, term))

    if row:
        return row[2]

    return None
