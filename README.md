# Budget-and-Expenses-Tracker-App
Capstone Project

This is a programme to manage budgets expenses and finance goals.

## Description

The first option in the main menu is 'Expenses' from which the user can
add expense, view expenses by category (over week, month or year) or
manage categories.  From the second main menu selection, 'Income' the
user can add income, view income or manage income sources.  From the
third menu selection, budget, the user can set overall budget (for
week, month or year), set budget by category (for week month or year),
view budgets or view budget progress (for week month or year). The last
menu choice 'Financial Goals' allows user to set gross or net income
goals or to view progress towards financial goals.  The latter will
display a graph with their progress for each week in the current year.

## Imports

* datetime
* dateutil
* matplotlib
* numpy
* os
* sqlite3
* time

## Overview

* main.py: entry point of programme
* main_menu.py: main menu options
* expenses.py: all logic for 'Expenses' menu
* income.py: all logic for 'Income' menu
* budget.py: all logic for 'Budget' menu
* goals.py: all logic for 'Goals' menu
* common_functions.py: functions used across multiple menu options
* date_functions.py: functions to get dates in specified ranges
* database_commands.py: all logic to interact with database
* populate_finances.py: adds dummy data for testing
* calcs.py: all calculations
* graphs.py: makes graphs
