import random

import walkers.healthState as h
import structures.locations as ls

class Walker:

    def __init__(self, width, height, age, disobedience, home, homeNode):
        self.status = h.SUSCEPTIBLE
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)
        self.healthLevel = random.uniform(0.2, 1)
        self.healingLevel = 0 # tasso di guarigione DAL VIRUS
        self.age = age
        self.disobedience = disobedience
        self.home = home #home object, may be omitted, or substituted with the current location to add another data
        self.homeNode = homeNode #index of home node
        self.loc = homeNode #conterrà la posizione attuale del walker
        
        # A coundown for disease
        self.TTL = -1
        self.wentForGroceries=False


        # maybe this part should be delegated to a function
        if self.isChild():
            if self.hasGoodHealth():
                self.pDisease = 0.9
                self.pDeath = 0
            elif self.hasBadHealth():
                self.pDisease = 0.7
                self.pDeath = 0.005
            else:
                self.pDisease = 0.8
                self.pDeath = 0.02

        elif self.isElder():
            if self.hasGoodHealth():
                self.pDisease = 0.4
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.1
                self.pDeath = 0.04
            else:
                self.pDisease = 0.25
                self.pDeath = 0.05
        else:
            if self.hasGoodHealth():
                self.pDisease = 0.6
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.3
                self.pDeath = 0.04
            else:
                self.pDisease = 0.45
                self.pDeath = 0.05


    def move(self, x, y):
        self.x = x
        self.y = y

    def isInA(self, engine, type):
        return isinstace(engine.gDict[self.loc], type)

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
        return self.status==h.INFECTED

    def isSubsceptible(self):
        return self.status == h.SUSCEPTIBLE

    def isRecovered(self):
        return self.status == h.RECOVERED

    def isChild(self):
        return self.age < h.young_age

    def isAdult(self):
        return self.age >= h.young_age and self.age < h.old_age

    def isElder(self):
        return self.age >= h.old_age

    def hasGoodHealth(self):
        return self.healthLevel >= h.goodHealth_level

    def hasMediumHealth(self):
        return self.healthLevel > h.badHealth_level and self.healthLevel < h.goodHealth_level

    def hasBadHealth(self):
        return self.healthLevel <= h.badHealth_level
