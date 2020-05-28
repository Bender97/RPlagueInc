import walkers.Walker
import walkers.healthState as h
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
            walker.setStatus(h.INCUBATION)
            return random.randint(2, 14)
        else:
            return 0

    def tryDisease(self, walker):
        if (walker.status!=h.INCUBATION):
            print("error in tryDisease: trying to infect a person without virus incubation")
            exit(1)
        if random.random() < walker.pDisease:
            walker.setStatus(h.INFECTED)
            return 1, random.randint(7, 28) # disease, disease_time
        else:
            walker.setStatus(h.ASYMPTOMATIC)
            return 0, random.randint(7, 28) # asymptomatic, asymptomatic_time

    def tryDeath(self, walker):
        if (walker.status!=h.INFECTED):
            print("error in tryDeath: trying to kill a person without virus infection!")
            exit(1)
        if random.random() < walker.pDeath:
            walker.setStatus(h.DEAD)
            return 1
        else:
            walker.setStatus(h.RECOVERED)
            return 0
    # commented FOR FURTHER WORKS
    #def computeDmg(self,walkerData): #walkerData contiene un vettore a cui verrà applicato il prodotto scalare con healthParams
    #    return np.inner(self.healthParams,walkerData)


