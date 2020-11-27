
#options=["-L","0.3", "-M", "0.2", "-N", "500", "-V", "0", "-S", "0", "-E", "20", "-H", "5"]
import os
import sys

sys.path
sys.path.append("/usr/lib/jvm/java-11-openjdk-amd64/bin/")
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
import weka.core.jvm as jvm
jvm.start()

from weka.classifiers import Evaluation
from weka.core.classes import Random
from weka.classifiers import Classifier
from weka.core.converters import Loader
from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from weka.core.classes import Random

loader = Loader("weka.core.converters.ArffLoader")
data = loader.load_file("AIProject/Database/WekaFiles/iris.arff")
data.class_is_last()
remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1-3"])

class Individual:
    def __init__(self, LearningR : float, Momentum : float, Period : int, HiddenLayers : list):
        self.LearningR = LearningR
        self.Momentum = Momentum
        self.Period = Period
        self.HiddenLayers = HiddenLayers
        self.FitnessValue = None
    def settings(self):
        Hlayers = ','.join(map(str, self.HiddenLayers)) 
        return ["-L",str(self.LearningR), "-M", str(self.Momentum), "-N", str(self.Period), "-V", "0", "-S", "0", "-E", "20", "-H", Hlayers]
    def tostr(self):
        Hlayers = ','.join(map(str, self.HiddenLayers)) 
        return 'options=["-L","{}", "-M", "{}", "-N", "{}", "-V", "0", "-S", "0", "-E", "20", "-H", "{}"]'.format(self.LearningR, self.Momentum, self.Period, Hlayers)


def fitness(toeval : Individual):
    cls = Classifier(classname="weka.classifiers.functions.MultilayerPerceptron", options=toeval.settings())
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = cls
    evl = Evaluation(data)
    evl.crossvalidate_model(fc, data, 10, Random(1))
    return evl.percent_correct


def randIndividual():
    return Individual(0.3, 0.2, 500, [5])  #falta hacerlo random


ind=Individual(0.3, 0.2, 500, [5,5])

ind.FitnessValue=fitness(ind)

print(ind.FitnessValue)

jvm.stop()