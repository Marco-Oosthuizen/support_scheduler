# Support Scheduler
This is a simple Genetic Algorithm that allocates developers to a fair support schedule, taking into consideration their leave days and public holidays.

## Basic usage
- Modify the `ScheduleParameters` object in the main method in `main.py` to suit the needs of the schedule to be generated, and run the program.
- The `seed` in the `GAParameters` object can be swapped to anything to produce different schedules.
- The lower the fitness of the produced schedule, the more optimized it is (and the less constraints it violates).

## Schedule Parameters
|Variable|Description|
|--------|-----------|
|`devs`|The list of developer names who will be allocated to production support|
|`dev_leave_days`|A dictionary that stores leave days per dev. Leave days can be either an individual `datetime` object, or if it is a range a tuple (`datetime`,`datetime`)|
|`schedule_start_date`|Starting date for the schedule to be generated|
|`schedule_end_date`|End date for the schedule to be generated|
|`dimensions`|How many devs should be allocated per day|

## GA Parameters
These are parameters for the Genetic Algorithm. Only tamper with if you have an understanding of GA's.
|Variable|Description|
|--------|-----------|
|`generations`|How many generations the GA should run for|
|`population_size`|How many individuals must be in the population|
|`crossover_rate`|Rate of crossover as a percentage out of 100|
|`mutation_rate1`|Rate of mutations as a percentage out of 100|
|`seed`|Random generator seed|
