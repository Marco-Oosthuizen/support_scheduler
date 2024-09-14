import random
from deap import creator, base, tools, algorithms
import fitness
import inputs


# Seed 3 does pretty good
seed = 3
generations = 200
population_size = 500
crossover_rate = 0.7
mutation_rate = 0.3


class Scheduler:
    def __init__(self, total_slots, devs, dev_availability):
        self.total_slots = total_slots
        self.devs = devs
        self.dev_availability = dev_availability
        self.available_devs_per_slot = inputs.get_available_devs_per_slot(total_slots, dev_availability)
        self.fitness = fitness.Fitness(total_slots, devs, dev_availability, self.available_devs_per_slot)

        random.seed(seed)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

    def evaluate(self, individual):
        roster = self.fitness.chromosome_to_roster(individual)
        penalty = self.fitness.fitness_func(roster)
        # print('Roster:', roster)
        # print('Fitness:', penalty)
        return penalty,

    def run_ga(self):
        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 255)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=self.total_slots)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=2)

        population = toolbox.population(n=population_size)

        for gen in range(generations):
            offspring = algorithms.varAnd(population, toolbox, cxpb=crossover_rate, mutpb=mutation_rate)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = toolbox.select(offspring, k=len(population))
            print('Best fitness for ', gen, ': ', tools.selBest(population, k=1)[0].fitness.values[0])
        best = tools.selBest(population, k=1)
        best_roster = self.fitness.chromosome_to_roster(best[0])
        print('Best single dimension roster', best_roster)
        best_fitness = self.fitness.fitness_func(best_roster)
        print('Best fitness:', best_fitness)
        return best_roster

    def generate_roster(self):
        final_roster = []
        for dimension in range(0, inputs.roster_dimensions):
            single_dimension_roster = self.run_ga()
            for slot in range(0, len(single_dimension_roster)):
                dev = single_dimension_roster[slot]
                if dev is None:
                    continue
                self.available_devs_per_slot[slot].remove(dev)
            final_roster.append(single_dimension_roster)
        print('Best multi-dimensional roster:', final_roster)
