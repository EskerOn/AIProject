import random

MAXDEC = 3 	# Cantidad de decimales en los float
MAXEP = 3000  	# Máximo de etapas
MINEP = 50		# Mínimo de etapas
NPARA = 13		# Cantidad de parámetros
NCLAS = 4		# Cantidad de clases
MAXCAP = 3      # Máximo de capas
SD = []
#Formato de genético
#list[x, y, z, v, w] : los rangos están de 0 a N y todos son int
# x neuronas x capa
# y capas
# z learningRate
# v momentum
# w etapas
# f fitnessValue no añadido aún

#Formato ANN list[z, v, w, [x, x, ..., x]] : los rangos ya están traducidos a los valores requeridos por WEKA

#Formato SD
"""valor limite               bits necesarios
|   neuronas x capa         |       x
|   capas                   |       x
|   decimales momentum      |       x
|   decimales learningRate  |       x
|   etapas                  |       x
"""

def initSD(): #inicializa los rangos de valores y bits de los atributos
    SD.append([NPARA, bitsTo(NPARA)])
    SD.append([MAXCAP,bitsTo(MAXCAP)])
    SD.append([pow(10, MAXDEC), bitsTo(pow(10, MAXDEC))])
    SD.append([pow(10, MAXDEC), bitsTo(pow(10, MAXDEC))])
    SD.append([MAXEP-MINEP,bitsTo(MAXEP-MINEP)])

def bitsTo(aux): #Dice cuántos bits son necesarios para un rango
    s = 1
    while(aux // 2 > 0):
        aux = aux//2
        s += 1
    return s


def translate(data : list):#Traduce el formato genético a ANN
	return [data[2]/pow(10, MAXDEC), data[3]/pow(10, MAXDEC), data[4] + MINEP, [data[0] + NCLAS for i in range(data[1] + 1)]] 


def randIndividual(): #genera el formato genético, línea 10
    aux = []
    for i in range(5):
        aux.append(random.randrange(SD[i][0]+1))
    return aux

def tobin(data : list):#Muestra la forma binaria
    out = ""
    for i in range(5):
        aux = bin(data[i])[2:]
        while(len(aux) < SD[i][1]):
            aux = "0"+aux
        out += aux
    return(out)

def mutation(data : list):#Hace una mutación en un parámetro aleatorio del individuo, trabaja sobre el formato genético
    out = [data[i] for i in range(5)]
    aux = random.randrange(5)
    print("voy a mutar el parámetro: ", aux)
    out[aux] = out[aux] | pow(2, random.randrange(SD[aux][1]))
    while(out[aux] > SD[aux][0]):
        out[aux] & pow(2, random.randrange(SD[aux][1]))
    return out


def fitness(data : list): #trabaja sobre el formato genético
    #aquí, de alguna manera se hace el llamado a WEKA
    #así que
    #return WEKA(translate(data))
    return random.randint(0, 100)

"""def GA(Fitness_threshold : float, P : int, R : float, M : int):
    population=[]
    populationS=[]
    for i in range(P):
        population.append(randIndividual())
    for element in population:
        element.FitnessValue=fitness(element)
    while():
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
    return max(population)"""


initSD()
print(SD)
aux = randIndividual()
print(aux)
print(translate(aux))
print(tobin(aux))
aux2 =  mutation(aux)
print("mutado\n", aux2)
print(translate(aux2))
print(tobin(aux2))
