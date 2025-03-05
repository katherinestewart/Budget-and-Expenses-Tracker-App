"""This module contains all functions with logic to interact with the
database finances.db. This is the only module which accesses the
database. There are six tables; expenses, income, categories, sources,
budget and goals.
"""

import sqlite3
from database import populate_finances_db

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
CREATE_INCOME_SOURCE_TABLE = """CREATE TABLE IF NOT EXISTS sources
(id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT)"""
ENTER_EXPENSE = """INSERT INTO expenses(date, expense, amount, categoryID)
VALUES(?,?,?,?)"""
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
ENTER_BUDGET = """INSERT INTO budget(amount, term) VALUES(?,?)"""
ENTER_CAT = """INSERT INTO categories(category) VALUES(?)"""
ENTER_GOAL = """INSERT INTO goals(goal, amount, term) VALUES(?,?,?)"""
ENTER_INCOME = """INSERT INTO income(date, sourceID, amount) VALUES(?,?,?)"""
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


def connect_db():
    """Establishes a connection to the SQLite database and returns the
    connection and cursor.

    :return: connection and cursor
    """
    try:
        conn = sqlite3.connect("finances.db")
        cursor_ = conn.cursor()
        return conn, cursor_
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None


def create_and_populate_tables():
    """This function creates all tables in the database if they don't
    exist.  If it is the first time they have been created, then it
    populates the table with dummy data.

    :return: None
    """
    db, cursor = connect_db()
    # Check if any tables exist in the database
    result = cursor.execute(TABLE_EXISTS).fetchone()

    cursor.execute(CREATE_EXPENSES_TABLE)
    cursor.execute(CREATE_CATEGORY_TABLE)
    cursor.execute(CREATE_INCOME_TABLE)
    cursor.execute(CREATE_INCOME_SOURCE_TABLE)
    cursor.execute(CREATE_BUDGET_TABLE)
    cursor.execute(CREATE_GOALS_TABLE)
    db.commit()

    # If no tables existed in the database at start up, then populate
    # tables with dummy data.
    if result is None:
        populate_finances_db.populate_tables()
        populate_finances_db.enter_budgets_goals()

    db.close()


def enter_expense(expense_tuple):
    """This function enters an expense into the expenses table.

    :param expense_tuple: tuple with date, expense, amount, categoryID
    :return: None
    """
    db, cursor = connect_db()
    cursor.execute(ENTER_EXPENSE, (*expense_tuple,))
    db.commit()
    db.close()


def enter_income(income_tuple):
    """This function enters an income into the income table.

    :param income_tuple: tuple with date, source, amount
    :return: None
    """
    db, cursor = connect_db()
    cursor.execute(ENTER_INCOME, (*income_tuple,))
    db.commit()
    db.close()


def enter_category(new_cat, table):
    """This function enters a new category in a table

    :param new_cat: new expense category or income source
    :param table: expenses or sources table in database
    :return: None
    """
    db, cursor = connect_db()

    if table == "categories":
        cursor.execute(ENTER_CAT, (new_cat,))
    else:
        cursor.execute(ENTER_SRC, (new_cat,))

    db.commit()
    db.close()


def get_row_list(table):
    """This function gets a list of all the rows in a table

    :param table: table in database
    :return: all rows
    :rtype: list
    """
    db, cursor = connect_db()
    cursor.execute(SELECT_ROWS.format(table))
    rows = cursor.fetchall()
    db.close()
    return rows


def get_rows(year_month, table):
    """This function gets all rows from a table, appends all rows to a
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
    :return: all rows from table
    :rtype: list of tuples
    """
    db, cursor = connect_db()

    if table == "expenses":
        cursor.execute(SELECT_EXPENSES)
    if table == "income":
        cursor.execute(SELECT_INCOME)
    if table == "categories":
        cursor.execute(SELECT_CATEGORIES)

    rows_list = cursor.fetchall()
    db.close()
    return rows_list


def get_category_from_id(category_id, table):
    """This function gets the description of an expenses category or
    income source from its id number

    :param category_id: primary key in table
    :param table: 'categories' or 'sources'
    :return: category
    :rtype: str
    """
    db, cursor = connect_db()

    if table == "categories":
        cursor.execute(SELECT_CATEGORY, (category_id,))
    if table == "sources":
        cursor.execute(SELECT_INC_CAT, (category_id,))

    category = cursor.fetchone()
    db.close()
    return category[0]


def get_category_from_budget(budget_id):
    """This function gets the category description, for a budget set by
    category, from its budget id number

    :param budget_id: budget primary key, category foreign key
    :return: category description or None
    :rtype: str or None
    """
    db, cursor = connect_db()
    cursor.execute(SEL_CAT_FROM_BUDG, (budget_id,))
    category = cursor.fetchone()

    if category:
        return category[0]

    db.close()
    return None


def get_max_budget_id():
    """This function gets the maximum value for primary key in budget
    table

    :return: max_id
    :rtype: int
    """
    db, cursor = connect_db()
    cursor.execute(MAX_BUDGET_ID)
    max_id = cursor.fetchone()
    db.close()
    return max_id


def update_category(table, cat_id, update):
    """This function updates a description for an expense category or
    an income source

    :param table: 'categories' or 'sources'
    :param cat_id: primary key id number
    :return: None
    """
    db, cursor = connect_db()

    if table == "categories":
        cursor.execute(CAT_UPDATE, (update, cat_id))
    if table == "sources":
        cursor.execute(SRC_UPDATE, (update, cat_id))

    db.commit()
    db.close()


def enter_budget(cat_id, amount, term):
    """This function enters a new budget assigned to a category

    :param cat_id: primary key in categories table
    :param amount: new budget amount
    :param term: "weekly", "monthly", or "annual"
    :return: None
    """
    db, cursor = connect_db()
    cat_rows = get_row_list("categories")

    for row in cat_rows:
        if row[0] == cat_id:
            cursor.execute(DELETE_BUDGET, (row[2],))

    cursor.execute(ENTER_BUDGET, (amount, term))
    budget_id = get_max_budget_id()
    cursor.execute(UPDATE_CAT_BUDGET, (*budget_id, cat_id))
    db.commit()
    db.close()


def get_expenses_date_amount(cat_id):
    """This function gets the date and amount of expenses from a chosen
    category

    :param cat_id: foreign key in expenses table, primary in categories
    :return: date and amount of expenses
    :rtype: list of tuples
    """
    db, cursor = connect_db()
    cursor.execute(SELECT_DATE_AMOUNT, (cat_id,))
    date_amount = cursor.fetchall()
    db.close()
    return date_amount


def get_expenses_by_date(days_list):
    """This function gets expenses for each day in a list

    :param days_list: list of days
    :return: list of rows from expenses table
    :rtype: list of tuples
    """
    db, cursor = connect_db()
    expenses_list = []

    for day in days_list:
        cursor.execute(SELECT_EXPS_BY_DATE, (day,))
        rows = cursor.fetchall()
        for row in rows:
            expenses_list.append(row)

    db.close()
    return expenses_list


def get_income_by_date(days_list):
    """This function gets income for each day in a list

    :param days_list: list of days
    :return: list of rows from income table
    :rtype: list of tuples
    """
    db, cursor = connect_db()
    income_list = []

    for day in days_list:
        cursor.execute(SELECT_INC_BY_DATE, (day,))
        rows = cursor.fetchall()
        for row in rows:
            income_list.append(row)

    db.close()
    return income_list


def enter_goal(goal, amount, term):
    """This function enters a new goal into the goals table

    :param goal: 'budget', 'net income' or 'gross income'
    :param amount: amount of money in goal
    :param term: 'weekly', 'monthly' or 'annual'
    :return: None
    """
    db, cursor = connect_db()

    if goal in ("net income", "gross income"):
        goals_list = get_row_list("goals")
        for row in goals_list:

            # Delete goal if one already exists
            if row[1] == goal:
                cursor.execute(DEL_GOAL, (row[0],))

    # Delete goal if one already exists
    if goal == "budget":
        cursor.execute(DELETE_GOAL, (goal, term))

    cursor.execute(ENTER_GOAL, (goal, amount, term))
    db.commit()
    db.close()


def get_goal(goal, term):
    """This function gets a goal amount from the goals table from its
    description and term

    :param goal: 'budget', 'net income' or 'gross income'
    :param term: 'weekly', 'monthly' or 'annual'
    :return: goal amount or None
    :rtype: float or None
    """
    db, cursor = connect_db()
    cursor.execute(SELECT_GOAL, (goal, term))
    row = cursor.fetchone()

    if row:
        return row[2]

    db.close()
    return None
