import random
from deap import creator, base, tools, algorithms
import fitness

# Seed 3 does pretty good
seed = 3
generations = 200
population_size = 500
crossover_rate = 0.7
mutation_rate = 0.3


class Scheduler:
    def __init__(self, schedule_request):
        self.schedule_request = schedule_request
        self.fitness = fitness.Fitness(schedule_request.total_slots, schedule_request.devs, schedule_request.dev_availability,
                                       schedule_request.available_devs_per_slot)

        random.seed(seed)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

    def evaluate(self, individual):
        roster = self.fitness.chromosome_to_roster(individual)
        individual_fitness = self.fitness.fitness_func(roster)
        return individual_fitness,

    def run_ga(self):
        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 255)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool,
                         n=self.schedule_request.total_slots)
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

    def generate_schedule(self):
        final_roster = []
        for dimension in range(0, self.schedule_request.dimensions):
            single_dimension_roster = self.run_ga()
            for slot in range(0, len(single_dimension_roster)):
                dev = single_dimension_roster[slot]
                if dev is None:
                    continue
                self.schedule_request.available_devs_per_slot[slot].remove(dev)
            final_roster.append(single_dimension_roster)
        print('Best multi-dimensional roster:', final_roster)
