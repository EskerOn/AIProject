import random
def randIndividual():
    return [0.3, 0.2, 500, [5]]  #falta hacerlo random

def fitness(some): #fitnes temporal
    return random.randint(0, 100)

def GA(Fitness_threshold : float, P : int, R : float, M : int):
    population=[]
    populationS=[]
    for i in range(P):
        population.append(randIndividual())
    for element in population:
        element.FitnessValue=fitness(element)
    while:
        sample=random.sample(population, int((1-R)*P))
        for item in sample:
            if(): ###aqui va la probabilidad Pr(hi)
                populationS.append(item)
        pairs=[(population[i],population[j]) for i in range(len(population)) for j in range(i+1, len(population))]
        sample=random.sample(pairs, int(R*P/2))
        for item in sample:
            if(): ###aqui va la probabilidad Pr(hi)
                pass ##aqui se hace el crosover
                ##se añaden a PopulationS
        sample=random.sample(populationS, int(len(populationS)/100*M))
        for item in sample:
            pass ##se aplica mutación sobre item
        population=populationS
        for element in population:
            element.FitnessValue=fitness(element)
    return max(population)