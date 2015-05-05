from random import randint, random
from operator import add
from functools import reduce

def individual(length,min,max):
    #creates an individual in the population
    #length is number of elements in list
    #min and max is the boundaries of each element
    return[ randint(min,max) for x in range(length) ]

def population(count,length,min,max):
    #count is the number of individuals in a population
    #length is the number of elements in the list
    #min and max are the boundaries of each element
    return[individual(length,min,max) for x in range(count)]

def fitness(individual, target):
    x = sum(individual)
    return abs(target-x)
    #returns absolute distance from target

def grade(pop, target):
    summed = reduce(add, (fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)
    #returns average distance of population from target

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    #retain is the threshold of the population that is closest to the target
    #random_select is a random selection of individuals to mix up the genomes
    #mutate is the mutation of random genes so that a new maximum can be found in the case a of a local maximum
    graded = [ (fitness(x, target), x) for x in pop]
    graded = [ x[1] for x in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # randomly adds other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male) / 2)
            child = male[:half] + female[half:]
            children.append(child)

    parents.extend(children)
    return parents

target = 371
p_count = 100
i_length = 5
i_min = 0
i_max = 100
p = population(p_count, i_length, i_min, i_max)
fitness_history = []
print("The Target number is:",target)
Go = True
final_vector = []
while (Go == True):
    p = evolve(p, target)
    print(p)
    print("**********************************************")
    x = grade(p,target)
    if (x == 0):
        fitness_history.append(x)
        Go = False
    else:
        fitness_history.append(grade(p, target))

number_of_tries = len(fitness_history)
z = 0
for datum in fitness_history:
    z = z+1
    print ("Generation",z,"Grade:",datum)
print("It took",number_of_tries,"generations to meet the target")
