import copy
import calendar_manager
from calendar_manager import day_to_index


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


def get_dev_availability(devs, leave_days_per_dev, workdays):
    dev_availability = {dev: [day for day in range(0, len(workdays))] for dev in devs}

    for dev, leave_days in leave_days_per_dev.items():
        for leave in leave_days:
            if isinstance(leave, tuple):
                start_date, end_date = leave
                leave_range = calendar_manager.get_workdays_between(start_date, end_date)
                for leave_day in leave_range:
                    dev_availability[dev].remove(day_to_index(leave_day, workdays))
            else:
                dev_availability[dev].remove(day_to_index(leave, workdays))

    return dev_availability


total_slots = 19
roster_dimensions = 1
dev_availability = {}

devs = list(dev_availability.keys())
total_available_slots_per_dev = get_total_available_slots_per_dev()
available_devs_per_slot = get_available_devs_per_slot(total_slots)
target_slots_per_dev = get_target_slots_per_dev(total_available_slots_per_dev)
