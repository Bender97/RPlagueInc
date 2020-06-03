"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import gym
from gym import spaces
import random
import numpy as np
import structures.locations as ls

import time

import structures.location as l
import engine.popgen as popgen
import engine.regiongen as reggen
from collections import defaultdict
import engine.statistics as stats

from engine.envs.render import *

import engine.virus as vir
from walkers.Walker import Walker

import walkers.healthState as h

import engine.schedules.schedules as schedules


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
        'video.frames_per_second': 50                       # not so true ..
    }

    # TODO
    def __init__(self):
        self.nLocation = None
        self.nHouses = None

        self.locs = [[], [], [], [], []]
        return

    def initialize(self, virus):
        
        if (self.nHouses == None):
            print("error: nHouses is None. Have you called reset() before calling initialize()?")
            exit(1)

        self.virus = virus

        self.closed_locs = []
        self.discontent = 0
        self.daily_discontent = 0

        self.safe_dist = 0
        self.quarantine = []

        self.shiftQueue = []        

        low = np.array([0, 0, 0, 0, -math.inf, 0, 0])
        high = np.array([+math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf, +math.inf])

        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.steps_done = None

    # end __init__
    ##################################################################

    def step(self, action):

        start_step = time.time()

        start_hours = time.time()

        for hour in range(0, 24):  # inizio delle 24 ore
            print("hour: " + str(hour))

            start_hour = time.time()

            for w in self.walker_list:
                # apply schedule entrypoint
                schedules.applySchedule(self, w, hour)


            end_hour = time.time()
            print("time elapsed for hour is: " + str(end_hour - start_hour))

            start_shift = time.time()
            # commit each shifted in the queue
            self.commitShift()
            end_shift = time.time()
            print("time elapsed for shift is: " + str(end_shift - start_shift))

            start_loc = time.time()
            # shift committed, it's time to run the hour
            l.run1HOUR(self)

            end_loc = time.time()
            print("time elapsed for location is: " + str(end_loc - start_loc))

            #renderFramePyGame(engine = self)
            #time.sleep(0.05)
                
        end_hours = time.time()
        print("time elapsed for day is:" + str(end_hours - start_hours))

        for loc in self.locs[ls.HOME]:
            loc.eatFood()
        
        start_inf = time.time()

        for locList in self.locs:
            for loc in locList:  # produce the deaths. tryInfection and tryDisease are called inside location file                
                for w in loc.walkers[h.INCUBATION]:
                    self.virus.tryDisease(w, self)
                for w in loc.walkers[h.ASYMPTOMATIC]:
                    self.virus.tryRecovery(w, self)
                for w in loc.walkers[h.INFECTED]:
                    self.virus.tryDeath(w, self)

        end_inf = time.time()
        print("time elapsed for infection is:" + str(end_inf - start_inf))

        end_step = time.time()
        print("time elapsed for step is: " + str(end_step - start_step))

        return list(stats.computeStatistics(self).items()), 1, False, {}

    def reset(self, nHouses):
        self.nHouses = nHouses

        self.walker_list = []
        
        reggen.regionGen(self)

        popgen.genPopulation(self)


        self.steps_done = 0

        self.deads = 0
        self.contact_list = {}

        # for pygame rendering
        self.screen = None
        self.fps = 0
        self.paused = False

        # calculate position on screen for each location
        self.locPos = [[], [], [], [], []]
        
        initPlt(self)
        initPyGame(self, border=20, padding = 20, name_of_window='Region')

        statistics = list(stats.computeStatistics(self).items())

        return statistics

    def render(self, mode='human'):
        renderFramePyGame(engine = self)
        renderFramePlt(engine = self)
        time.sleep(0.1)

    # def close(self):

    def goToLoc(self, walker, locType):
        self.shiftQueue.append((walker, locType))

    def commitShift(self):
        for elem in self.shiftQueue:
            locType = elem[1]
            walker = elem[0]

            if (locType == ls.HOME):
                walker.exit()
                walker.enter(walker.home)
            elif (locType == ls.WORKPLACE):            
                walker.exit()
                walker.enter(walker.workPlace)
            elif (locType == ls.SCHOOL):
                walker.exit()
                walker.enter(walker.school)
            elif (locType == ls.LEISURE):
                target = random.randint(0, len(self.locs[ls.LEISURE]) -1)
                walker.exit()
                walker.enter(self.locs[ls.LEISURE][target])
                
            elif (locType == ls.GROCERIES_STORE):
                target = random.randint(0, len(self.locs[ls.GROCERIES_STORE])-1)
                walker.exit()
                walker.enter(self.locs[ls.GROCERIES_STORE][target])
                #print("Ora sono a" , walker.loc)
                food = walker.home.family_qty * random.randint(3, 7)
                walker.home.money -= walker.loc.buyFood(food)
                walker.home.bringFood(food)

        self.shiftQueue = []