import copy


def get_total_available_slots_per_dev():
    d = dict(dev_availability)
    for dev, slots in d.items():
        d[dev] = len(slots)
    return d


def get_available_devs_per_slot(total_slots):
    available_devs_per_slot = {}
    for dev, slots in dev_availability.items():
        for slot in slots:
            if slot not in available_devs_per_slot:
                available_devs_per_slot[slot] = []
            available_devs_per_slot[slot].append(dev)
    available_devs_per_slot_sorted_by_slot = {}
    first_slot = 0
    last_slot = total_slots - 1

    for slot in range(first_slot, last_slot + 1):
        available_devs_per_slot_sorted_by_slot[slot] = available_devs_per_slot.get(slot, [])

    return available_devs_per_slot_sorted_by_slot


def get_target_slots_per_dev(available_slots_per_dev):
    target_slots_per_dev = {dev: 0 for dev in devs}

    available_slots_per_dev_clone = copy.deepcopy(available_slots_per_dev.copy())
    available_slots_grouped_by_available_devs = list(set(available_slots_per_dev_clone.values()))
    available_slots_grouped_by_available_devs.sort()
    slots_catered_for = 0
    for available_slots in available_slots_grouped_by_available_devs:
        available_devs = [dev for dev, slots in available_slots_per_dev_clone.items() if slots > 0]
        available_slots -= slots_catered_for
        for dev in available_devs:
            target_slots_per_dev[dev] += round(available_slots / len(available_devs))
            available_slots_per_dev_clone[dev] -= available_slots
        slots_catered_for += available_slots

    return target_slots_per_dev


def get_dev_availability(devs, leave_days_per_dev, total_slots):
    for dev, leave_days in leave_days_per_dev.items():
        for leave_range in leave_days:

    return


total_slots = 19
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
total_available_slots_per_dev = get_total_available_slots_per_dev()
available_devs_per_slot = get_available_devs_per_slot(total_slots)
target_slots_per_dev = get_target_slots_per_dev(total_available_slots_per_dev)
