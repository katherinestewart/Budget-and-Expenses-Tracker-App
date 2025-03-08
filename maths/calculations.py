"""This module contains functions with the logic for all mathematical
calculations used in the programme. All functions take in floats and
return floats rounded to 2 decimal places.
"""


def total_spending(amount_list):
    """This function calculates the total from a list of amounts

    :param amount_list: list of float amounts
    :return: sum of all amounts in list
    :rtype: float
    """
    total = 0

    for amount in amount_list:
        total += amount

    return round(total, 2)


def difference(small_num, big_num):
    """This function calculates the difference between two values

    :param num1: float number
    :param num2: float number
    :return: difference between num1 and num2
    :rtype: float
    """
    answer = big_num - small_num
    return round(answer, 2)


def annual_from_weekly(weekly_amount):
    """This function calculates an annual amount from a weekly amount

    :param weekly_amount: amount per week
    :return: amount per annum
    :rtype: float
    """
    answer = weekly_amount * 52
    return round(answer, 2)


def annual_from_monthly(monthly_amount):
    """This function calculates a monthly amount over a year

    :param monthly_amount: amount per month
    :return: amount per year
    :rtype: float
    """
    answer = monthly_amount * 12
    return round(answer, 2)


def get_mean(numbers_list):
    """This function calculates the mean from a list of numbers

    :param numbers_list: list of numbers
    :return: mean of the numbers in the list
    :rtype: float
    """
    total = 0
    for i in numbers_list:
        total += i

    answer = total / len(numbers_list)
    return answer


def get_week_from_year(amount):
    """This function takes in an amount over an annual term and returns
    the amount for one week

    :param amount: amount over a year
    :return: amount of money over a week
    :rtype: float
    """
    answer = amount / 52
    return answer


def get_month_from_year(amount):
    """This function takes in an amount over an annual term and returns
    the amount for one month

    :param amount: amount over a year
    :return: amount over a month
    :rtype: float
    """
    answer = amount / 12
    return answer
