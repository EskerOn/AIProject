import random

###Temporal para hacer pruebas
class Individual:
    def __init__(self, LearningR : float, Momentum : float, Period : int, HiddenLayers : list):
        self.LearningR = LearningR
        self.Momentum = Momentum
        self.Period = Period
        self.HiddenLayers = HiddenLayers
        self.FitnessValue = None
        self.GeneticForm = None
    def settings(self):
        Hlayers = ','.join(map(str, self.HiddenLayers)) 
        return ["-L",str(self.LearningR), "-M", str(self.Momentum), "-N", str(self.Period), "-V", "0", "-S", "0", "-E", "20", "-H", Hlayers]
    def __str__(self):
        Hlayers = ','.join(map(str, self.HiddenLayers)) 
        return 'options=["-L","{}", "-M", "{}", "-N", "{}", "-V", "0", "-S", "0", "-E", "20", "-H", "{}"]'.format(self.LearningR, self.Momentum, self.Period, Hlayers)

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

def fitness(toeval : Individual): 
    return random.randint(0, 100)

class GeneticA():
    def __init__(self, MAXDEC, MAXEP, MINEP, NATRIB, NCLAS, MAXCAP, FITNESS):
        self.settings=[MAXDEC, MAXEP, MINEP, NATRIB, NCLAS, MAXCAP]
        self.SD=[]
        self.SD.append([NATRIB, self.bitsTo(NATRIB)])
        self.SD.append([MAXCAP-1,self.bitsTo(MAXCAP-1)])
        self.SD.append([pow(10, MAXDEC)-50, self.bitsTo(pow(10, MAXDEC)-50)])
        self.SD.append([pow(10, MAXDEC)-50, self.bitsTo(pow(10, MAXDEC)-50)])
        self.SD.append([MAXEP-MINEP, self.bitsTo(MAXEP-MINEP)])
        #GA()
    def bitsTo(self, aux): #Dice cuántos bits son necesarios para un rango
        s = 1
        while(aux // 2 > 0):
            aux = aux//2
            s += 1
        return s

    def translate(self, data : list):#Traduce el formato genético a ANN
        return [data[2]/pow(10, self.settings[0]), data[3]/pow(10, self.settings[0]), data[4] + self.settings[2], [data[0] + self.settings[5] for i in range(data[1] + 1)]]

    def randIndividual(self): #genera el formato genético, línea 10
        aux = []
        for i in range(5): 
            aux.append(random.randrange(self.SD[i][0]+1))
        ind=Individual(aux[2]/pow(10, self.settings[0]), aux[3]/pow(10, self.settings[0]), aux[4] + self.settings[2], [aux[0] + self.settings[5] for i in range(aux[1] + 1)])
        ind.GeneticForm=aux
        return ind

    def tobin(self, data : list):#Muestra la forma binaria del formato genético
        out = ""
        for i in range(5):
            out += self.tobins(data[i], self.SD[i][1])
        return(out)

    def tobins(self, a : int, size : int): #Muestra la forma binaria de un número
        out = bin(a)[2:]
        while(len(out) < size):
                out = "0"+out
        return out

    def toformgen(self, genes : int):
        out = []
        for i in range(5):
            mask = (1 << self.SD[4-i][1]) - 1
    #        out.append(genes & mask)
            out.insert(0, genes & mask)
            genes = genes >> self.SD[4-i][1]
        for i in range(5):
            if out[i]>self.SD[i][0]:
                print("------------------------fuera de rango {} ".format(out[i]))
                out[i]=self.SD[i][0]
        ind=Individual(out[2]/pow(10, self.settings[0]), out[3]/pow(10, self.settings[0]), out[4] + self.settings[2], [out[0] + self.settings[5] for i in range(out[1] + 1)])
        ind.GeneticForm=out
        return ind

    def mutation(self, data : list):#Hace una mutación en un parámetro aleatorio del individuo, trabaja sobre el formato genético
        out = [i for i in data]
        aux = random.randrange(5)
        print("voy a mutar el parámetro: ", aux)
        maskaux = pow(2, self.SD[aux][1]) - 1
        mask = pow(2, random.randrange(self.SD[aux][1]))  
        if mask & data[aux] > 0:#bit encendido
            out[aux] = ((data[aux] ^ maskaux) | mask) ^ maskaux
        else:
            out[aux] = data[aux] | mask
        while(out[aux] > self.SD[aux][0]):
            mask = pow(2, random.randrange(self.SD[aux][1]))  
            if mask & data[aux] > 0:#bit encendido
                out[aux] = ((data[aux] ^ maskaux) | mask) ^ maskaux
            else:
                out[aux] = data[aux] | mask
        ind=Individual(out[2]/pow(10, self.settings[0]), out[3]/pow(10, self.settings[0]), out[4] + self.settings[2], [out[0] + self.settings[5] for i in range(out[1] + 1)])
        ind.GeneticForm=out
        return ind

    def cruza(self, padre : list, madre : list):#Recibe dos formatos genéticos y devuelve uno resultado de los dos
        padres = self.tobin(padre)
        madres = self.tobin(madre)
        punto = random.randrange(3, len(padres) - 3)
        print("punto de cruza: ", punto)
        mask1 = (1 << punto) - 1
        mask2 = ((1 << (len(padres)-punto)) - 1) << punto
        h1 = (int(padres, 2) & mask1) | (int(madres, 2) & mask2)
        h2 = (int(padres, 2) & mask2) | (int(madres, 2) & mask1)
        return self.toformgen(h1), self.toformgen(h2)

    def pr(self, val):
        return random.randint(0, 100)

    def maxim(self, population):
        maxitem=population[0]
        for item in population:
            if item.FitnessValue>maxitem.FitnessValue:
                maxitem=item
        return maxitem

    def GA(self, Fitness_threshold : float, P : int, R : float, M : int, fitness):
        population=[]
        populationS=[]
        for i in range(P):
            population.append(self.randIndividual())
        for element in population:
            element.FitnessValue=fitness(element)
        iteraciones=0
        while(iteraciones<5000):
            sample=random.sample(population, int((1-R)*P))
            for item in sample:
                if(self.pr(item)): ###aqui va la probabilidad Pr(hi)
                    populationS.append(item)
            pairs=[(population[i],population[j]) for i in range(len(population)) for j in range(i+1, len(population))]
            sample=random.sample(pairs, int(R*P/2))
            for item in sample:
                if(self.pr(item)): ###aqui va la probabilidad Pr(hi)
                    h1, h2 = self.cruza(item[0].GeneticForm, item[1].GeneticForm)
                    populationS.append(h1)
                    populationS.append(h2)
            sample=random.sample(populationS, int(len(populationS)/100*M))
            for item in sample:
                item = self.mutation(item.GeneticForm) ##se aplica mutación sobre item
            population=populationS
            for element in population:
                element.FitnessValue=fitness(element)
            iteraciones+=1
        return self.maxim(population)

MAXDEC = 2 	# Cantidad de decimales en los float
MAXEP = 500  	# Máximo de etapas
MINEP = 50		# Mínimo de etapas
NATRIB = 13		# Cantidad de parámetros
NCLAS = 4		# Cantidad de clases
MAXCAP = 3      # Máximo de capas


gen=GeneticA(MAXDEC, MAXEP, MINEP, NATRIB, NCLAS, MAXCAP, fitness)
#print(SD)
#ejemplos
aux = gen.randIndividual()
print("dos individuos aleatorios, ya cumplen con el rango")
print(aux)
aux2 = gen.randIndividual()
print(aux2)
print("su representación binaria")
print(gen.tobin(aux.GeneticForm))
print(gen.tobin(aux2.GeneticForm))
print("los resultados de la cruza, no necesariamente cimplen el rango")
h1, h2 = gen.cruza(aux.GeneticForm, aux2.GeneticForm)
print(h1)
print(h2)
print("su representación binaria")
print((gen.tobin(h1.GeneticForm)))
print((gen.tobin(h2.GeneticForm)))
m1 = gen.mutation(h1.GeneticForm)
print("mutacion del hijo 1")
print(m1)
print(gen.tobin(m1.GeneticForm))
