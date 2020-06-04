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
            return random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1])
        else:
            return 0

    def tryDisease(self, walker, engine):
        if (walker.status!=h.INCUBATION):
            print("error in tryDisease: trying to infect a person without virus incubation")
            exit(1)

        walker.updateVirusTimer()

        if walker.getVirusTimer() <= 0:
            
            walker.loc.walkers[h.INCUBATION].remove(walker)
            
            if random.random() < walker.pDisease:
                walker.setStatus(h.INFECTED)
                walker.updateVirusTimer(value = random.randint(h.DISEASE_DURATION_RANGE[0], h.DISEASE_DURATION_RANGE[1]))
                walker.loc.walkers[h.INFECTED].append(walker)
                
                if walker.infectedBy in engine.contact_list:
                    engine.contact_list[walker.infectedBy] += 1
                elif walker.infectedBy != None:
                    engine.contact_list[walker.infectedBy] = 1
                return 1
            
            else:
                walker.setStatus(h.ASYMPTOMATIC)
                walker.updateVirusTimer(value = random.randint(h.ASYMPTOMATIC_DURATION_RANGE[0], h.ASYMPTOMATIC_DURATION_RANGE[1]))
                walker.loc.walkers[h.ASYMPTOMATIC].append(walker)
                return 0

    def tryRecovery(self, walker, engine):
        walker.updateVirusTimer()
        if (walker.getVirusTimer() <= 0):
            walker.loc.walkers[h.ASYMPTOMATIC].remove(walker)
            walker.loc.walkers[h.RECOVERED_FROM_ASYMPTOMATIC].append(walker)
            walker.setStatus(h.RECOVERED_FROM_ASYMPTOMATIC)

    def tryDeath(self, walker, engine):
        if (walker.status!=h.INFECTED):
            print("error in tryDeath: trying to kill a person without virus infection!")
            exit(1)
        
        walker.updateVirusTimer()

        if walker.getVirusTimer() <= 0:
            walker.loc.walkers[h.INFECTED].remove(walker)
            
            if random.random() < walker.pDeath:
                walker.setStatus(h.DEAD)
                walker.loc = None
                engine.deads += 1
                engine.walker_pool.remove(walker)
                return 1
            else:
                walker.setStatus(h.RECOVERED_FROM_INFECTED)
                walker.loc.walkers[h.RECOVERED_FROM_INFECTED].append(walker)
                if walker not in engine.contact_list:
                    engine.contact_list[walker] = 0
                return 0
    # commented FOR FURTHER WORKS
    #def computeDmg(self,walkerData): #walkerData contiene un vettore a cui verrà applicato il prodotto scalare con healthParams
    #    return np.inner(self.healthParams,walkerData)


