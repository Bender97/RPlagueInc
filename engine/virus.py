import walkers.Walker
import parameters as param
import random
import numpy as np

class Virus:
    def __init__(self,range, pInfection, severity, lethality):
        self.range = range
        self.pInfection = pInfection
        self.severity = severity
        self.lethality = lethality

    def tryInfection(self,walker):
        if walker.isSusceptible() and random.random() < self.pInfection:
            walker.setStatus(param.INCUBATION)
            return random.randint(param.INCUBATION_DURATION_RANGE[0], param.INCUBATION_DURATION_RANGE[1])
        else:
            return 0

    def tryDisease(self, walker, engine):
        if (walker.status!=param.INCUBATION):
            print("error in tryDisease: trying to infect a person without virus incubation")
            exit(1)

        walker.updateVirusTimer()

        if walker.getVirusTimer() <= 0:
            
            walker.loc.walkers[param.INCUBATION].remove(walker)
            
            if random.random() < (walker.pDisease + self.severity) * self.severity:
                walker.setStatus(param.INFECTED)
                walker.updateVirusTimer(value = random.randint(param.DISEASE_DURATION_RANGE[0], param.DISEASE_DURATION_RANGE[1]))
                walker.loc.walkers[param.INFECTED].append(walker)

                if walker.infectedBy in engine.contact_list:
                    engine.contact_list[walker.infectedBy] += 1
                elif walker.infectedBy != None:
                    engine.contact_list[walker.infectedBy] = 1
                return 1
            
            else:
                walker.setStatus(param.ASYMPTOMATIC)
                walker.updateVirusTimer(value = random.randint(param.ASYMPTOMATIC_DURATION_RANGE[0], param.ASYMPTOMATIC_DURATION_RANGE[1]))
                walker.loc.walkers[param.ASYMPTOMATIC].append(walker)
                return 0

    def tryRecovery(self, walker, engine):
        walker.updateVirusTimer()
        if (walker.getVirusTimer() <= 0):
            walker.loc.walkers[param.ASYMPTOMATIC].remove(walker)
            walker.loc.walkers[param.RECOVERED_FROM_ASYMPTOMATIC].append(walker)
            walker.setStatus(param.RECOVERED_FROM_ASYMPTOMATIC)

    def tryDeath(self, walker, engine):
        if (walker.status!=param.INFECTED):
            print("error in tryDeath: trying to kill a person without virus infection!")
            exit(1)
        
        walker.updateVirusTimer()

        if walker.getVirusTimer() <= 0:
            walker.loc.walkers[param.INFECTED].remove(walker)

            #if walker not in engine.contact_list:
            #    engine.contact_list[walker] = 0
            
            if random.random() < (walker.pDeath + self.lethality) * self.lethality:
                walker.setStatus(param.DEAD)
                walker.loc = None
                engine.deads += 1
                engine.walker_pool.remove(walker)
                return 1
            else:
                walker.setStatus(param.RECOVERED_FROM_INFECTED)
                walker.loc.walkers[param.RECOVERED_FROM_INFECTED].append(walker)
                return 0
    # commented FOR FURTHER WORKS
    #def computeDmg(self,walkerData): #walkerData contiene un vettore a cui verrà applicato il prodotto scalare con healthParams
    #    return np.inner(self.healthParams,walkerData)


