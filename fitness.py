from collections import Counter

import inputs
from inputs import *


def fitness_func(primary_roster):
    penalty = 0
    penalty += penalties_for_load(primary_roster)
    penalty += penalties_for_preference(primary_roster)
    penalty += penalties_for_spread(primary_roster)
    return penalty


def penalties_for_load(primary_roster):
    target_days_per_dev = dict(available_days_per_dev)
    for dev, days in target_days_per_dev.items():
        target_days_per_dev[dev] = 0
    calculate_target_days_for_devs(target_days_per_dev)
    support_days_per_dev = dict(Counter(primary_roster))
    penalty = 0
    for dev, support_days in support_days_per_dev.items():
        penalty += abs(support_days - target_days_per_dev[dev])
    return penalty


def calculate_target_days_for_devs(target_days_per_dev):
    available_days_per_dev_clone = available_days_per_dev.copy()
    days_segments = list(set(available_days_per_dev_clone.values()))
    days_segments.sort()
    days_catered_for = 0
    for segment in days_segments:
        available_devs = [dev for dev, days in available_days_per_dev_clone.items() if days > 0]
        segment -= days_catered_for
        for dev in available_devs:
            target_days_per_dev[dev] += round(segment / len(available_devs))
            available_days_per_dev_clone[dev] -= segment
        days_catered_for += segment


def penalties_for_preference(primary_roster):
    weighting = 2
    preferred_indices = [2, 3, 7, 8, 12, 13, 17]
    juan_indices = [index for index, dev in enumerate(primary_roster) if dev == 'Juan']
    penalty = len([actual_index for actual_index in juan_indices if actual_index not in preferred_indices])*weighting
    return penalty


def penalties_for_spread(primary_roster):
    weighting = 0.5
    penalty = 0
    ideal_spread = len(devs)
    for dev in devs:
        last_seen_index = -1
        for index, name in enumerate(primary_roster):
            if name == dev:
                if last_seen_index > -1:
                    current_spread = index - last_seen_index
                    penalty += 0 if current_spread >= ideal_spread else (ideal_spread - current_spread)
                last_seen_index = index
    penalty *= weighting
    return penalty


def chromosome_to_roster(chromosome):
    roster = []
    index = 0
    available_devs_per_day = inputs.get_availability_dev()
    for codon in chromosome:
        available_devs = len(available_devs_per_day[index])
        if available_devs == 0:
            roster.append(None)
            continue
        dev = available_devs_per_day[index].pop(codon % available_devs)
        roster.append(dev)
        index += 1
        if index == total_days:
            break
    return roster
