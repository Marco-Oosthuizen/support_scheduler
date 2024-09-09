import copy


def get_total_available_days_per_dev():
    d = dict(dev_availability)
    for dev, days in d.items():
        d[dev] = len(days)
    return d


def get_available_devs_per_day(total_days):
    available_devs_per_day = {}
    for dev, days in dev_availability.items():
        for day in days:
            if day not in available_devs_per_day:
                available_devs_per_day[day] = []
            available_devs_per_day[day].append(dev)
    available_devs_per_day_sorted_by_day = {}
    first_day = 0
    last_day = total_days - 1

    for day in range(first_day, last_day + 1):
        available_devs_per_day_sorted_by_day[day] = available_devs_per_day.get(day, [])

    return available_devs_per_day_sorted_by_day


def get_target_days_per_dev(available_days_per_dev):
    target_days_per_dev = {dev: 0 for dev in devs}

    available_days_per_dev_clone = copy.deepcopy(available_days_per_dev.copy())
    available_days_grouped_by_available_devs = list(set(available_days_per_dev_clone.values()))
    available_days_grouped_by_available_devs.sort()
    days_catered_for = 0
    for available_days in available_days_grouped_by_available_devs:
        available_devs = [dev for dev, days in available_days_per_dev_clone.items() if days > 0]
        available_days -= days_catered_for
        for dev in available_devs:
            target_days_per_dev[dev] += round(available_days / len(available_devs))
            available_days_per_dev_clone[dev] -= available_days
        days_catered_for += available_days

    return target_days_per_dev


total_days = 19
dev_availability = {
    'William': [10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Mokgali': [0, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Marco': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18],
    'Natasha': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18],
    'Juan': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Vuyani': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
}

roster_dimensions = 1
devs = list(dev_availability.keys())
total_available_days_per_dev = get_total_available_days_per_dev()
available_devs_per_day = get_available_devs_per_day(total_days)
target_days_per_dev = get_target_days_per_dev(total_available_days_per_dev)
