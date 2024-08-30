def get_available_days_per_dev():
    d = dict(dev_availability)
    for dev, days in d.items():
        d[dev] = len(days)
    return d


devs = ['Marco', 'William', 'Mokgali', 'Natasha', 'Juan', 'Vuyani']
dev_availability = {
    'William': [10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Mokgali': [0, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Marco': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18],
    'Natasha': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18],
    'Juan': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    'Vuyani': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
}
available_days_per_dev = get_available_days_per_dev()
total_days = 19


def get_availability_dev():
    availability_dev = {}
    for dev, days in dev_availability.items():
        for day in days:
            if day not in availability_dev:
                availability_dev[day] = []
            availability_dev[day].append(dev)

    # Sort the keys and add missing keys with empty lists
    sorted_availability_dev = {}
    min_key = min(availability_dev.keys())
    max_key = max(availability_dev.keys())

    for i in range(min_key, max_key + 1):
        sorted_availability_dev[i] = availability_dev.get(i, [])

    # print(sorted_availability_dev)
    return sorted_availability_dev
