import random
from deap import creator, base, tools, algorithms
import fitness
from inputs import total_days


# Seed 3 does pretty good
seed = 3
generations = 200
crossover_rate = 0.7
mutation_rate = 0.3


def evaluate(individual):
    roster = fitness.chromosome_to_roster(individual)
    penalty = fitness.fitness_func(roster)
    # print('Roster:', roster)
    # print('Fitness:', penalty)
    return penalty,


def run_ga():
    random.seed(seed)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("attr_bool", random.randint, 0, 255)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=total_days)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=2)

    population = toolbox.population(n=500)

    for gen in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=crossover_rate, mutpb=mutation_rate)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        print('Best fitness for ', gen, ': ', tools.selBest(population, k=1)[0].fitness.values[0])
    best = tools.selBest(population, k=1)
    best_roster = fitness.chromosome_to_roster(best[0])
    print('Best roster', best_roster)
    best_fitness = fitness.fitness_func(best_roster)
    print('Best fitness:', best_fitness)