from datetime import datetime
import calendar_manager
import ga
import inputs


def receive_inputs():
    month = 9
    year = 2024

    work_days = calendar_manager.get_workdays_between(datetime(year, month, 2), datetime(year, month, 27))
    print(work_days)
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


if __name__ == '__main__':
    receive_inputs()
    ga.generate_roster()

