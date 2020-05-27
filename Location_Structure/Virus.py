import Walker
import healthState as h
import random
import numpy as np

class Virus:
    def __init__(self,range, pInfection, healthParams, healingParams):
        self.range = range
        self.pInfection = pInfection
        self.healthParams = healthParams #parametri funzione affine di "danno"
        self.healingParams = healingParams #parametri funzione affine di "guarigione"

    def tryInfection(self,walker):
        if random.random() < self.pInfection:
            walker.setStatus(h.INFECTED)
            return 1
        else:
            return 0

    def computeDmg(self,walkerData): #walkerData contiene un vettore a cui verrà applicato il prodotto scalare con healthParams
        return np.inner(self.healthParams,walkerData)


