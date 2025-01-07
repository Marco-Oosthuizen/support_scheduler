from support_scheduler.utilities import calendar_utilities


def print_schedule(schedule, workdays):
    dimensions = len(schedule)
    total_days = len(schedule[0])
    vertical_margins = '-------------------------------------------------'

    print('\n\n')
    print(vertical_margins)
    for day in range(0, total_days):
        date = calendar_utilities.get_date_for_schedule_slot(day, workdays)
        weekday = date.strftime('%a')
        day_of_month = date.strftime('%d')
        month = date.strftime('%m')
        schedule_for_day = '\t|\t'.join([f'{schedule[dimension][day]}' for dimension in range(0, dimensions)])
        print(f'{weekday}-{month}/{day_of_month}\t|\t{schedule_for_day}\t|')
    print(vertical_margins)


def get_formatted_schedule(schedule, workdays):
    dimensions = len(schedule)
    total_days = len(schedule[0])

    formatted_schedule = []
    for day in range(0, total_days):
        date = calendar_utilities.get_date_for_schedule_slot(day, workdays)
        schedule_for_day = [schedule[dimension][day] for dimension in range(0, dimensions)]
        formatted_schedule.append({date: schedule_for_day})

    return formatted_schedule
