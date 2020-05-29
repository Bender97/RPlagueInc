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
import structures.locations as l
import networkx as nx
import structures.location as l
import engine.popgen as popgen
import engine.regiongen as reggen
from collections import defaultdict


import engine.virus as vir
from walkers.Walker import Walker


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
    def __init__(self, nLocation, virus):

        self.nLocation = nLocation
        self.steps_done = 0
        self.gDict = nx.get_node_attributes(self.region) #dict that links nodes to locations objects

        self.virus = virus

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        low = np.array([0, 0, 0, 0, -math.inf, 0, 0])
        high = np.array([+math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf])

        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    # end __init__



    def step(self, action):
        gDict= self.gDict #giusto per non scrivere self ogni volta xD
        for hour in range(0,24): #inizio delle 24 ore
            for loc in gDict.values(): #for every location
                for w in loc.walkers:
                    if w.isAdult:
                        if (random.rand() < self.adultHomeProbFcn(hour)) or w.wentForGroceries:
                            self.goHome(w)  # if already at home, nothing happens
                            w.wentForGroceries=False
                        else:
                            atHome = (w.homeNode == w.loc)
                            if atHome:
                                if(w.home.needFood() and (8<=hour<=10 or 17<=hour<=19)):
                                    self.leave(w,l.GROCERIES_STORE)
                                    #buy
                                    w.wentForGroceries=True
                                else: #altre cose per il worker
                                    activity=np.random.ch

            l.run1HOUR(self.virus)
        for loc in gDict.values():  #produce the deaths. tryInfection and tryDisease are called inside location file
            for w in loc.walkers:
                w.updateVirusTimer()
                if w.getVirusTimer() ==0:
                    self.virus.tryDeath(w) #no need to do anything else, if he doesn't die the counter will be resetted to -1 at the next iteration
        #inserire modifiche apportate dall'azione al resto dell'engine, da fare alla fine della giornata (in questo punto del codice)

    ##################################################################

    def reset(self, nLocation):
        self.region = reggen.regionGen(nLocation)
        popgen.genPopulation(self.region)
        self.steps_done = 0
        self.nLocation = nLocation


    #def render(self, mode='human'):




    def adultHomeProbFcn(self,hour): #hour-dependent,prob to go/stay home
        if(hour==12):
            return 0.50
        else:
            return 1-((math.fabs(hour-12)*2)/24.0)

    #def childHomeProbFcn(self,hour):
        #if(7 <= hour <=)
        #else : #coprifuoco
            #return 1

    #def close(self):

    def goToNearestLoc(self, walker, locType): #movimento dalla posizione attuale al posto selezionato più vicino
            pathsDict = defaultdict(list)
            found = False
            gDict= self.gDict #giusto per non scrivere self ogni volta xD
            paths= nx.shortest_path(self.region, source=walker.pos)
            for i in range(0,self.nLocation):
                if paths[i].length() >0:
                    pathsDict[paths[i].lenght].append(i)
            for len in sorted(pathsDict.keys()):
                for dest in pathsDict[len]:
                        #scandisce la lista dai nodi più vicini ai più lontani
                        if locType==l.WORKPLACE and isinstance(gDict[dest],l.Workplace):
                            walker.home.exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found=True
                            break
                        elif locType==l.SCHOOL and isinstance(gDict[dest],l.School):
                            walker.home.exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found = True
                            break
                        elif locType==l.GROCERIES_STORE and isinstance(gDict[dest],l.GroceriesStore):
                            walker.home.exit(walker)
                            gDict[dest].enter(walker)
                            walker.loc = dest
                            found = True
                            break
                        elif locType ==l.LEISURE and isinstance(gDict[dest],l.Leisure):
                            walker.home.exit(walker)
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

