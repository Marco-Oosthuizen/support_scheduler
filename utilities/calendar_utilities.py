import calendar
from datetime import datetime, timedelta
import holidays


public_holidays = holidays.country_holidays('ZA')


def get_workdays_for_year_and_month(year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    workdays = []

    for day in range(1, days_in_month + 1):
        weekday = datetime(year, month, day).weekday()
        if weekday < 5 and datetime(year, month, day) not in public_holidays:
            workdays.append(day)

    return workdays


def get_workdays_between(start_date, end_date, return_as_num=False):
    workdays = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in public_holidays:
            workdays.append(current_date)
        current_date += timedelta(days=1)

    return len(workdays) if return_as_num else workdays


def get_schedule_slot_for_date(date, workdays):
    return workdays.index(date)


def get_date_for_schedule_slot(slot, workdays):
    return workdays[slot]
