import os
import sys
from datetime import datetime
import calendar_manager
import ga
import inputs


# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
    sys.stdout = sys.__stdout__


def setup_output(show_output):
    if show_output:
        enable_print()
    else:
        block_print()


if __name__ == '__main__':
    show_output = True
    setup_output(show_output)

    month = 9
    year = 2024

    work_days = calendar_manager.get_workdays_between(datetime(year, month, 2), datetime(year, month, 27))
    inputs.total_slots = len(work_days)

    devs = ['William', 'Mokgali', 'Marco', 'Natasha', 'Juan', 'Vuyani']
    leave_days_per_dev = {
        'William': [(datetime(year, month, 2), datetime(year, month, 13))],
        'Mokgali': [(datetime(year, month, 4), datetime(year, month, 10))],
        'Marco': [datetime(year, month, 23)],
        'Natasha': [datetime(year, month, 23)],
        'Vuyani': [(datetime(year, month, 25), datetime(year, month, 27))]
    }
    dev_availability = inputs.get_dev_availability(devs, leave_days_per_dev, work_days)
    print(dev_availability)

    scheduler = ga.Scheduler(19, devs, dev_availability)
    scheduler.generate_roster()

