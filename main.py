from datetime import datetime

import calendar_manager
import ga
import inputs


def receive_inputs():
    month = 9

    work_days = calendar_manager.get_workdays_between(datetime(2024, month, 2), datetime(2024, month, 27))
    print(work_days)
    inputs.total_slots = len(work_days)

    devs = ['William', 'Mokgali', 'Marco', 'Natasha', 'Juan', 'Vuyani']
    leave_days_per_dev = {
        'William': [(datetime(2024, month, 2), datetime(2024, month, 13))],
        'Mokgali': [(datetime(2024, month, 4), datetime(2024, month, 10))],
        'Marco': [(datetime(2024, month, 23), datetime(2024, month, 23))],
        'Natasha': [(datetime(2024, month, 23), datetime(2024, month, 23))],
    }


if __name__ == '__main__':
    receive_inputs()
    ga.generate_roster()

