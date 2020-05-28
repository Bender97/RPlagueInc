import random

import walkers.healthState as h


class Walker:

    def __init__(self, width, height,age,disobedience,home):
        self.status = h.SUSCEPTIBLE
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)
        self.healthLevel = random.uniform(0.7, 1)
        self.healingLevel = 0 # tasso di guarigione DAL VIRUS
        self.age = age
        self.disobedience = disobedience
        self.home = home
        # just for testing, 2 lines to be deleted
        self.pDisease = 0
        self.pDeath = 0

        # maybe this part should be delegated to a function
        if self.isChild():
            if self.hasGoodHealth():
                self.pDisease = 0.02
                self.pDeath = 0
            elif self.hasBadHealth():
                self.pDisease = 0.002
                self.pDeath = 0.005
            else:
                self.pDisease = 0.04
                self.pDeath = 0.02

        elif self.isElder():
            if self.hasGoodHealth():
                self.pDisease = 0.015
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.025
                self.pDeath = 0.04
            else:
                self.pDisease = 0.03
                self.pDeath = 0.05
        else:
            if self.hasGoodHealth():
                self.pDisease = 0.02
                self.pDeath = 0.03
            elif self.hasBadHealth():
                self.pDisease = 0.035
                self.pDeath = 0.04
            else:
                self.pDisease = 0.045
                self.pDeath = 0.05


    def move(self, x, y):
        self.x = x
        self.y = y

    def setStatus(self, status):
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