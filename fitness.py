import copy
import dev_utilities
from collections import Counter


class Fitness:
    def __init__(self, total_slots, devs, dev_availability, available_devs_per_slot):
        self.devs = devs
        self.total_slots = total_slots
        self.available_devs_per_slot = available_devs_per_slot
        self.target_slots_per_dev = dev_utilities.get_target_slots_per_dev(devs, dev_availability)

    def fitness_func(self, schedule):
        penalty = 0
        penalty += self.penalties_for_load(schedule)
        penalty += self.penalties_for_preference(schedule)
        penalty += self.penalties_for_spread(schedule)
        return penalty

    def penalties_for_load(self, primary_schedule, weight=1):
        allocated_slots_per_dev = dict(Counter(primary_schedule))
        penalty = 0
        for dev, allocated_support_slots in allocated_slots_per_dev.items():
            if dev is None:
                continue
            penalty += abs(allocated_support_slots - self.target_slots_per_dev[dev])
        return penalty * weight

    def penalties_for_preference(self, primary_schedule, weight=2):
        preferred_indices = [2, 3, 7, 8, 12, 13, 17]
        juan_indices = [index for index, dev in enumerate(primary_schedule) if dev == 'Juan']
        penalty = len([actual_index for actual_index in juan_indices if actual_index not in preferred_indices])
        return penalty * weight

    def penalties_for_spread(self, primary_schedule, weight=0.5):
        penalty = 0
        ideal_spread = len(self.devs)
        for dev in self.devs:
            last_support_slot = -1
            for current_slot, name in enumerate(primary_schedule):
                if name == dev:
                    if last_support_slot > -1:
                        current_spread = current_slot - last_support_slot
                        penalty += 0 if current_spread >= ideal_spread else (ideal_spread - current_spread)
                    last_support_slot = current_slot
        return penalty * weight

    def chromosome_to_schedule(self, chromosome):
        schedule = []
        available_devs_per_slot = copy.deepcopy(self.available_devs_per_slot)
        for index in range(0, len(chromosome)):
            codon = chromosome[index]
            available_devs = len(available_devs_per_slot[index])
            if available_devs == 0:
                schedule.append(None)
                continue
            dev = available_devs_per_slot[index].pop(codon % available_devs)
            schedule.append(dev)
            if index == self.total_slots:
                break
        return schedule
