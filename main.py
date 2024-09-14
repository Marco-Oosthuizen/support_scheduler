import os
import sys
from datetime import datetime
import ga
from request import ScheduleParameters, GAParameters


def block_print():
    sys.stdout = open(os.devnull, 'w')


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
    schedule_parameters = ScheduleParameters(
        schedule_start_date=datetime(year, month, 2),
        schedule_end_date=datetime(year, month, 27),
        devs=['William', 'Mokgali', 'Marco', 'Natasha', 'Juan', 'Vuyani'],
        dev_leave_days={
            'William': [(datetime(year, month, 2), datetime(year, month, 13))],
            'Mokgali': [(datetime(year, month, 4), datetime(year, month, 10))],
            'Marco': [datetime(year, month, 23)],
            'Natasha': [datetime(year, month, 23)],
            'Vuyani': [(datetime(year, month, 25), datetime(year, month, 27))]
        },
        dimensions=2,
    )

    # Seed 3 does pretty good
    ga_parameters = GAParameters(
        seed=3,
        generations=200,
        population_size=500,
        crossover_rate=0.7,
        mutation_rate=0.3,
    )

    scheduler = ga.Scheduler(schedule_parameters, ga_parameters)
    scheduler.generate_schedule()
