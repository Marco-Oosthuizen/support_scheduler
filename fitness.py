import copy
from collections import Counter
import inputs


def fitness_func(primary_roster):
    penalty = 0
    penalty += penalties_for_load(primary_roster)
    penalty += penalties_for_preference(primary_roster)
    penalty += penalties_for_spread(primary_roster)
    return penalty


def penalties_for_load(primary_roster, weight=1):
    allocated_days_per_dev = dict(Counter(primary_roster))
    penalty = 0
    for dev, allocated_support_days in allocated_days_per_dev.items():
        penalty += abs(allocated_support_days - inputs.target_days_per_dev[dev])
    return penalty * weight


def penalties_for_preference(primary_roster, weight=2):
    preferred_indices = [2, 3, 7, 8, 12, 13, 17]
    juan_indices = [index for index, dev in enumerate(primary_roster) if dev == 'Juan']
    penalty = len([actual_index for actual_index in juan_indices if actual_index not in preferred_indices])
    return penalty * weight


def penalties_for_spread(primary_roster, weight=0.5):
    penalty = 0
    ideal_spread = len(inputs.devs)
    for dev in inputs.devs:
        last_support_day = -1
        for current_day, name in enumerate(primary_roster):
            if name == dev:
                if last_support_day > -1:
                    current_spread = current_day - last_support_day
                    penalty += 0 if current_spread >= ideal_spread else (ideal_spread - current_spread)
                last_support_day = current_day
    return penalty * weight


def chromosome_to_roster(chromosome):
    roster = []
    index = 0
    available_devs_per_day = copy.deepcopy(inputs.available_devs_per_day)
    for codon in chromosome:
        available_devs = len(available_devs_per_day[index])
        if available_devs == 0:
            roster.append(None)
            continue
        dev = available_devs_per_day[index].pop(codon % available_devs)
        roster.append(dev)
        index += 1
        if index == inputs.total_days:
            break
    return roster
