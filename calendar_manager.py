import calendar
from datetime import datetime
import holidays


def get_workdays(year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    workdays = []
    public_holidays = holidays.country_holidays('ZA')
    public_holiday_dates = [date.day for date in public_holidays]

    for day in range(1, days_in_month + 1):
        weekday = datetime(year, month, day).weekday()

        if weekday < 5 and datetime(year, month, day) not in public_holidays:
            workdays.append(day)
    return workdays, public_holiday_dates

