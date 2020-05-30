"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import gym
from gym import spaces, logger
import random
import numpy as np
import structures.locations as ls
import networkx as nx
import structures.location as l
import engine.popgen as popgen
import engine.regiongen as reggen
from collections import defaultdict
import engine.statistics as stats


import engine.virus as vir
from walkers.Walker import Walker

import time
import matplotlib.pyplot as plt
import walkers.healthState as h


class EngineEnv(gym.Env):
    """
    Description:
        A region contains several locations, which contains walkers.
        The engine simulates the infection in this region. Each day is represented as
        a step(). Each step run several update() of each location
    Observation:
        Type: Box(7)
        Num	Observation             Min         Max
        0	Susceptibles            0           POP_NUM
        1   Infected                0           POP_NUM
        2   Recovered               0           POP_NUM
        3   Deads                   0           POP_NUM
        4   Discontent              -infinite   +infinite
        5   Population Money Avg    0           +infinite
        6   R0                      0           +infinite
    Actions:
        Type: Discrete(7)
        Num	Action
        0   No Operation
        1   Mandatory Mask
        2   Mandatory Safe Distance
        3   Quarantine for Infected Walkers
        4   Close Schools
        5   Close Leasures
        6   Close Workplaces
    Reward:
        Reward = -discontent + 1/R0 - R0 - deads + Money Avg
    Starting State:
        Susceptibles starts from the totality of the population minus some starting infected
        Infected starts from some randomly selected
        No recovered, no deads, no discontent
    Episode Termination:
        1   All deads
        2   Termination steps reached
        3   The virus has gone extinct
    Solved Requirements:
        Considered solved when the average reward is greater than or equal to
        a Success Quantity over 100 consecutive trials.
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    # TODO
    def __init__(self):
        return

    def initialize(self, nLocation, virus):
        self.nLocation = nLocation
        self.virus = virus
        self.gDict = nx.get_node_attributes(self.region, 'LocType') #dict that links nodes to locations objects

        self.virus = virus

        self.day_counter = 0
        self.xdata = []
        self.ydata = [[], [], [], []]

        low = np.array([0, 0, 0, 0, -math.inf, 0, 0])
        high = np.array([+math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf])

        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)


        self.steps_done = None
    # end __init__



    def step(self, action):
        
        gDict= self.gDict #giusto per non scrivere self ogni volta xD
        
        for hour in range(0,24): #inizio delle 24 ore
            for loc in gDict.values(): #for every location
                for walkerType in range(6):
                    for w in loc.walkers[walkerType]:
                        #Adult Schedule
                        if w.isAdult():
                            if (random.random() < self.adultHomeProbFcn(hour)) or w.wentForGroceries:
                                self.goHome(w)  # if already at home, nothing happens
                                w.wentForGroceries=False
                            else:
                                atHome = (w.homeNode == w.loc)
                                if atHome:
                                    if(w.home.needFood() and (8<=hour<=10 or 17<=hour<=19)) and random.random() < (1 - w.disobedience):
                                        self.goToNearestLoc(w,ls.GROCERIES_STORE)
                                        w.wentForGroceries=True
                                        food = w.home.family_qty * random.randint(3,7)
                                        w.home.money-=self.gDict[w.loc].buyFood(food)
                                        w.home.bringFood(food)
                                        break
                                activityLoc=np.random.choice([ls.WORKPLACE,ls.LEISURE] , p=[0.75,0.25])
                                self.goToNearestLoc(w,activityLoc)
                        #Child
                        elif w.isChild():
                            if not(7<=hour<=19) or w.wentForGroceries:
                                self.goHome(w)
                                w.wentForGroceries = False
                            elif(7<=hour<=8):
                                if w.loc == w.homeNode:
                                    if random.random() < 0.7:
                                        self.goToNearestLoc(w,ls.SCHOOL)
                            elif(hour ==9):
                                if w.loc == w.homeNode:
                                    self.goToNearestLoc(w,ls.SCHOOL)
                            elif(13<=hour<=14):
                                if w.loc != w.homeNode:
                                    if random.random() < 0.5:
                                        self.goToNearestLoc(w,ls.SCHOOL)
                            elif(hour==15):
                                if w.loc != w.homeNode:
                                    self.goHome(w)
                            elif(16<=hour<=19):
                                if w.loc == w.homeNode:
                                    if w.home.needFood() and random.random() < (1 - w.disobedience):
                                        self.goToNearestLoc(w, ls.GROCERIES_STORE)
                                        w.wentForGroceries = True
                                        food = w.home.family_qty * random.randint(3, 7)
                                        w.home.money -= self.gDict[w.loc].buyFood(food)
                                        w.home.bringFood(food)
                                        break
                                    if random.random()<0.6:
                                        self.goToNearestLoc(w,ls.LEISURE) #go out and play a little
                                else:
                                    if random.random()<0.4:
                                        self.goHome(w)
                        #Elder
                        else:
                            if not(7<=hour<=19) or w.wentForGroceries:
                                self.goHome(w)
                                w.wentForGroceries = False
                            else:
                                if w.loc == w.homeNode:
                                    if w.home.needFood() and random.random() < (1 - w.disobedience):
                                        try:
                                            print(self.gDict[w.loc])
                                            self.goToNearestLoc(w, ls.GROCERIES_STORE)
                                            w.wentForGroceries = True
                                            food = w.home.family_qty * random.randint(3, 7)
                                            w.home.money -= self.gDict[w.loc].buyFood(food)
                                            w.home.bringFood(food)
                                            break
                                        except:
                                            print(self.gDict[w.loc])
                                            exit()
                                    if random.random() < 0.4:
                                            self.goToNearestLoc(w, ls.LEISURE)
                                else:
                                    if random.random() < 0.6:
                                            self.goHome(w)
            loc.run1HOUR(self.virus)
        
        for loc in gDict.values():  #produce the deaths. tryInfection and tryDisease are called inside location file
            if isinstance(loc,ls.Home):
                loc.eatFood()
                for w in loc.walkers[h.INFECTED]:
                    w.updateVirusTimer()
                    if w.getVirusTimer() ==0:
                        flag = self.virus.tryDeath(w) #no need to do anything else, if he doesn't die the counter will be resetted to -1 at the next iteration
        #inserire modifiche apportate dall'azione al resto dell'engine, da fare alla fine della giornata (in questo punto del codice)
                        if (flag):
                            self.deads += 1

        return list(stats.computeStatistics(self).items()), 1, False, {}

    ##################################################################

    def reset(self, nLocation):
        self.region = reggen.regionGen(nLocation)
        popgen.genPopulation(self.region)
        self.steps_done = 0
        self.nLocation = nLocation

        self.deads = 0

        self.contact_list = {}

        Gdict = nx.get_node_attributes(self.region, 'LocType')
        for key in Gdict.keys():
            for statusType in range(6):
                for walker in Gdict[key].walkers[statusType]:
                    self.contact_list[walker] = 0

        statistics = list(stats.computeStatistics(self).items())

        return statistics

    def render(self, mode='human'):
        Gdict = nx.get_node_attributes(self.region, 'LocType')
        
        #loc = Gdict[0]

        statistics = list(stats.computeStatistics(self).items())

        self.xdata.append(self.day_counter)

        self.ydata[0].append(statistics[0][1])
        self.ydata[1].append(statistics[1][1])
        self.ydata[2].append(statistics[2][1])
        self.ydata[3].append(statistics[3][1])
        
        plt.plot(self.xdata, self.ydata[0], 'bo-')
        plt.plot(self.xdata, self.ydata[1], 'ro-')
        plt.plot(self.xdata, self.ydata[2], 'go-')
        plt.plot(self.xdata, self.ydata[3], 'ko-')

        self.day_counter += 1
        plt.pause(0.1)


    def adultHomeProbFcn(self,hour): #hour-dependent,prob to go/stay home
        if(hour==12):
            return 0.50
        else:
            return 1-((math.fabs(hour-12)*2)/24.0)

    def childHomeProbFcn(self,hour):
        if(7 <= hour <=9):
            return 0.5
        elif(10 <= hour <=14):
            return 0
        elif(15 <= hour <=17):
            return 0.5
        else : #coprifuoco
            return 1

    #def close(self):

    def goToNearestLoc(self, walker, locType): #movimento dalla posizione attuale al posto selezionato più vicino
            pathsDict = defaultdict(list)
            found = False
            gDict= self.gDict #giusto per non scrivere self ogni volta xD

            paths= nx.shortest_path(self.region, source=walker.loc)

            for key in paths.keys():
                if len(paths[key])>1:
                    pathsDict[len(paths[key])].append(key)
            
            for length in sorted(pathsDict.keys()):
                for dest in pathsDict[length]:
                        #scandisce la lista dai nodi più vicini ai più lontani
                        if locType==ls.WORKPLACE and isinstance(gDict[dest],ls.Workplace):
                            gDict[walker.loc].exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found=True
                            break
                        elif locType==ls.SCHOOL and isinstance(gDict[dest],ls.School):
                            gDict[walker.loc].exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found = True
                            break
                        elif locType==ls.GROCERIES_STORE and isinstance(gDict[dest],ls.GroceriesStore):
                            gDict[walker.loc].exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found = True
                            break
                        elif locType ==ls.LEISURE and isinstance(gDict[dest],ls.Leisure):
                            gDict[walker.loc].exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found = True
                            break
                if found:
                    break

    def goHome(self, walker): # torna a casa (se non ci è già)
        if not(walker.loc == walker.homeNode):
            self.gDict[walker.loc].exit(walker)
            walker.home.enter(walker)
            walker.loc = walker.homeNode

