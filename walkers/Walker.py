import random
import numpy as np

import parameters as param


class Walker:

    def __init__(self, age, disobedience, home, dutyPlace):
        self.status = param.SUSCEPTIBLE
        self.index = None
        self.healthLevel = random.uniform(0.2, 1)
        self.healingLevel = 0 # tasso di guarigione DAL VIRUS
        self.age = age
        self.disobedience = disobedience        # low level: obedient
                                                # high level: disobedient, also: it listens to Justin Bieber, too strong
        self.home = home

        if self.isChild():
            self.school = dutyPlace
        elif not self.isElder():    # that is, if it's an adult (1 if less)
            self.workPlace = dutyPlace

        self.loc = self.home
        
        # A coundown for disease
        self.TTL = -1
        self.infectedBy = None

        self.wentForGroceries=False


        # maybe this part should be delegated to a function
        # remember there is also the virus stats severity and lethality

        self.pDisease = self.age / 100 * 0.5 + (1 - self.healthLevel) * 0.5
        self.pDeath = self.age / 100 * 0.5 + (1 - self.healthLevel) * 0.5
        '''
        if self.isChild():
            if self.hasGoodHealth():
                self.pDisease = 0
                self.pDeath = 0
            elif self.hasBadHealth():
                self.pDisease = 0.3
                self.pDeath = 0.005
            else:
                self.pDisease = 0.2
                self.pDeath = 0.02

        elif self.isElder():
            if self.hasGoodHealth():
                self.pDisease = 0.4
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.8
                self.pDeath = 0.04
            else:
                self.pDisease = 0.6
                self.pDeath = 0.05
        else:
            if self.hasGoodHealth():
                self.pDisease = 0.3
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.7
                self.pDeath = 0.04
            else:
                self.pDisease = 0.5
                self.pDeath = 0.05
        '''
       

    # updates the status with a 1 day time step.Has to be called from engine.
    #Has to work with tryDeath, when the counter reaches 0.
    def updateVirusTimer(self, value = None):
        if(value != None):
            self.TTL = value
        elif (self.TTL>-1):
            self.TTL-=1

    def getVirusTimer(self):
        return self.TTL

    def setStatus(self, status): #useless at this point
        self.status = status

    def isInfected(self):
        return self.status==param.INFECTED

    def isSusceptible(self):
        return self.status == param.SUSCEPTIBLE

    def isRecovered(self):
        return self.status == param.RECOVERED_FROM_INFECTED

    def isChild(self):
        return self.age < param.young_age

    def isAdult(self):
        return self.age >= param.young_age and self.age < param.old_age

    def isElder(self):
        return self.age >= param.old_age

    def hasGoodHealth(self):
        return self.healthLevel >= param.goodHealth_level

    def hasMediumHealth(self):
        return self.healthLevel > param.badHealth_level and self.healthLevel < param.goodHealth_level

    def hasBadHealth(self):
        return self.healthLevel <= param.badHealth_level

    def spawnCoords(self):
        width = self.loc.size_x
        height = self.loc.size_y
        return [random.randint(0,width), random.randint(0,height)]


class WalkerPool:

    def __init__(self):
        self.walker_list = []
        self.coord_list = []
    # end __init__

    def add(self, walker):
        walker.index = len(self.walker_list)
        self.walker_list.append(walker)
        self.coord_list.append([0, 0])
    # end add

    def remove(self, walker):
        for i in range(walker.index + 1, self.getWalkerNum()):
            self.walker_list[i].index -= 1

        self.coord_list.pop(walker.index)
        self.walker_list.pop(walker.index)
    # end remove

    def exit(self, walker):
        walker.loc.walkers[walker.status].remove(walker)
        walker.loc = None
    # end exit

    def enter(self, walker, target):
        target.walkers[walker.status].append(walker)
        walker.loc = target
        self.coord_list[walker.index] = walker.spawnCoords()
    # end enter

    def getCoords (self, walker):
        return self.coord_list[walker.index]
    # end getCoords

    def getWalkerNum (self):
        return len(self.walker_list)