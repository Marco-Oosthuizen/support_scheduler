import random
from deap import creator, base, tools, algorithms
import fitness


class Scheduler:
    def __init__(self, schedule_parameters, ga_parameters):
        self.schedule_params = schedule_parameters
        self.fitness = fitness.Fitness(schedule_parameters.total_slots, schedule_parameters.devs, 
                                       schedule_parameters.dev_availability, 
                                       schedule_parameters.available_devs_per_slot)

        self.ga_params = ga_parameters

        random.seed(self.ga_params.seed)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

    def evaluate(self, individual):
        schedule = self.fitness.chromosome_to_schedule(individual)
        individual_fitness = self.fitness.fitness_func(schedule)
        return individual_fitness,

    def run_ga(self):
        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 255)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool,
                         n=self.schedule_params.total_slots)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=2)

        population = toolbox.population(n=self.ga_params.population_size)

        for gen in range(self.ga_params.generations):
            offspring = algorithms.varAnd(population, toolbox, cxpb=self.ga_params.crossover_rate,
                                          mutpb=self.ga_params.mutation_rate)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = toolbox.select(offspring, k=len(population))
            print('Best fitness for ', gen, ': ', tools.selBest(population, k=1)[0].fitness.values[0])
        best = tools.selBest(population, k=1)
        best_schedule = self.fitness.chromosome_to_schedule(best[0])
        print('Best single dimension schedule', best_schedule)
        best_fitness = self.fitness.fitness_func(best_schedule)
        print('Best fitness:', best_fitness)
        return best_schedule

    def generate_schedule(self):
        final_schedule = []
        for dimension in range(0, self.schedule_params.dimensions):
            single_dimension_schedule = self.run_ga()
            for slot in range(0, len(single_dimension_schedule)):
                dev = single_dimension_schedule[slot]
                if dev is None:
                    continue
                self.schedule_params.available_devs_per_slot[slot].remove(dev)
            final_schedule.append(single_dimension_schedule)
        print('Best multi-dimensional schedule:', final_schedule)
