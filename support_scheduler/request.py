from support_scheduler.utilities import calendar_utilities, dev_utilities


class ScheduleParameters:
    def __init__(self, schedule_start_date, schedule_end_date, devs, dev_leave_days, dev_preferred_days=None, dimensions=1):
        if dev_preferred_days is None:
            dev_preferred_days = {}
        self.schedule_start_date = schedule_start_date
        self.schedule_end_date = schedule_end_date
        self.workdays = calendar_utilities.get_workdays_between(schedule_start_date, schedule_end_date)
        self.total_slots = len(self.workdays)

        self.devs = devs
        self.dev_leave_days = dev_leave_days
        self.dev_availability_matrix = dev_utilities.get_dev_availability_matrix(devs, dev_leave_days, self.workdays)
        self.available_devs_per_slot = dev_utilities.get_available_devs_per_slot(self.total_slots,
                                                                                 self.dev_availability_matrix)

        self.dev_preferred_slots = None if dev_preferred_days is None else dev_utilities.get_dev_preferred_slots(
            dev_preferred_days, self.dev_availability_matrix, self.workdays)

        self.dimensions = dimensions


class GAParameters:
    def __init__(self, seed, generations, population_size, crossover_rate, mutation_rate):
        self.seed = seed
        self.generations = generations
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
