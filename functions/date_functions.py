"""This module contains functions with the logic for finding date
ranges from user input.

References
----------
[1] Tutorials Point (for function get_week_dates)
https://www.tutorialspoint.com/How-to-find-only-Monday-s-date-with-Python#:~:text=the%20dateutil%20module.-,Use%20the%20today()%20function%20(gets%20the%20current%20local%20date,Print%20the%20last%20Monday%20date.  # noqa
"""

import datetime
from dateutil.relativedelta import relativedelta, MO
from functions import common_functions


YEAR_MENU = """\nView progress for:
1.  Week
2.  Month
3.  Year
0.  Return to main menu
\nEnter your selection: \
"""


def get_days_list(term):
    """This function gets a list of days over a given term

    :param term: 'weekly', 'monthly' or 'annual'
    :return: list of dates
    :rtype: list of str
    """
    term_dict = {
        "weekly": get_week_dates(),
        "monthly": get_month_dates(),
        "annual": get_year_dates(),
    }
    return term_dict[term]


def get_week_dates():
    """This function gets last Monday's date, makes a new list and
    appends last Monday. It then calls function to get dates before
    last Monday

    :return: function to get dates before last Monday
    :rtype: func
    """
    day = datetime.date.today()
    last_monday = day - relativedelta(weekday=MO(-1))
    days_list = [day.strftime("%Y-%m-%d")]

    return get_dates(last_monday, days_list)


def get_month_dates():
    """This function finds the first day of the current month, appends
    it to a list. It then returns function to get dates for previous
    months

    :return: returns function to get dates for previous months
    :rtype: func
    """
    day = datetime.date.today()
    first_day = day.replace(day=1)
    days_list = [day.strftime("%Y-%m-%d")]

    return get_dates(first_day, days_list)


def get_year_dates():
    """This function gets the first day of this year and returns
    function to get days between then and now

    :return: function to get a list of days since start of year
    :rtype: func
    """
    day = datetime.date.today()
    first_month = day.replace(month=1)
    first_day = first_month.replace(day=1)
    days_list = [day.strftime("%Y-%m-%d")]

    return get_dates(first_day, days_list)


def get_dates(first_day, days_list):
    """This function gets dates for days that have passed since a given
    day and appends them to a list of days

    :param first_day: day in the past
    :return: list of days since first_day
    :rtype: list of str
    """
    day = datetime.date.today()

    while first_day <= day:
        # Roll back one day
        day = day - datetime.timedelta(days=1)
        days_list.append(day.strftime("%Y-%m-%d"))

    return days_list


def get_dates_for_goals():
    """This function gets user selection for term and calls relevant
    function

    :return: None
    """
    term = common_functions.get_term(YEAR_MENU)
    if term == "annual":
        get_date_of_first_day_each_week_this_year()


def get_date_of_first_day_each_week_this_year():
    """This function gets the first day of each week in the current
    year starting from 1st Jan up until today's date.

    :return: list of first day of week for this year
    :rtype: list of str
    """
    day = datetime.date.today()
    first_day = day.replace(day=1)
    first_month = first_day.replace(month=1)
    dates_list = []

    while first_month <= day:
        dates_list.append(first_month)
        first_month += datetime.timedelta(days=7)

    return dates_list


def all_dates_in_week(date):
    """This function takes in a date and returns that date plus the
    next six days.

    :param date: a date
    :return: dates for week
    :rtype: list of dates
    """
    day = datetime.date.today()
    dates_for_week = [date]
    i = 0

    for i in range(6):
        date = date + datetime.timedelta(days=1)
        if date <= day:
            dates_for_week.append(date)
        i += 1

    return dates_for_week
