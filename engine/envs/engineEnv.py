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

import engine.choices as choices

from engine.envs.render import *

import engine.virus as vir
from walkers.Walker import Walker, WalkerPool

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

        high = np.array([np.finfo(np.float32).max,
                         np.finfo(np.float32).max,
                         np.finfo(np.float32).max,
                         np.finfo(np.float32).max,
                         np.finfo(np.float32).max,
                         np.finfo(np.float32).max],
                        dtype=np.float32)
        low = np.array([0,
                         0,
                         0,
                         0,
                         0,
                         0],
                        dtype=np.float32)

        self.action_space = spaces.Discrete(choices.N_CHOICES)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        return

    def initialize(self, virus, nHouses):
        
        self.nHouses = nHouses
        #if (self.nHouses == None):
        #    print("error: nHouses is None. Have you called reset() before calling initialize()?")
        #    exit(1)

        self.virus = virus

        self.shiftQueue = []


    # end __init__
    ##################################################################

    def step(self, action):

        start_step = time.time()

        death_derivative = -self.deads

        start_hours = time.time()

        for hour in range(0, 24):  # inizio delle 24 ore
            #print("hour: " + str(hour))

            start_hour = time.time()

            for w in self.walker_pool.walker_list:
                # apply schedule entrypoint
                schedules.applySchedule(self, w, hour)


            end_hour = time.time()
            #print("time elapsed for hour is: " + str(end_hour - start_hour))

            start_shift = time.time()
            # commit each shifted in the queue
            self.commitShift()
            end_shift = time.time()
            #print("time elapsed for shift is: " + str(end_shift - start_shift))

            start_loc = time.time()
            # shift committed, it's time to run the hour
            l.run1HOUR(self)

            end_loc = time.time()
            #print("time elapsed for location is: " + str(end_loc - start_loc))

            #renderFramePyGame(engine = self)
            #time.sleep(0.05)
                
        end_hours = time.time()
        #print("time elapsed for day is:" + str(end_hours - start_hours))

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
        #print("time elapsed for infection is:" + str(end_inf - start_inf))

        #Agent Choice(Edo)

        self.discontent += self.daily_discontent
        print ("Discontent of the day = " + str(self.discontent))

        death_derivative+=self.deads
        statistics = stats.computeStatistics(self)
        st = dict(statistics.items())
        exist_recovered=False
        for w in self.walker_pool.walker_list:
            if w.isRecovered():
                exist_recovered= True
                break
        if(exist_recovered):
            finished = self.isDone(st)
        else:
            finished = False
        if(st[stats.R0]!=0):
            reward = (-1/20.0)* self.discontent + (1/float(st[stats.R0])) - st[stats.R0] -(1/5.0) * death_derivative +(1/2.0)*st[stats.M]
        else: #caso iniziale, in cui ci sono solo incubati
            reward = (-1/20.0)* self.discontent -(1/5.0) * death_derivative +(1/2.0)*st[stats.M]

        self.steps_done +=1
        self.discontent = 0

        end_step = time.time()
        #print("time elapsed for step is: " + str(end_step - start_step))

        return list(statistics.values()), reward, finished, {}


    def reset(self):

        self.walker_pool = WalkerPool()
        
        self.locs = [[], [], [], [], []]
        reggen.regionGen(self)

        popgen.genPopulation(self)

        self.closed_locs = []
        self.discontent = 0
        self.daily_discontent = 0

        self.safe_dist = 0
        self.quarantine = []

        choices.setupChoices(self)

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

        statistics = list(stats.computeStatistics(self).values())

        return statistics

    def render(self, mode='human'):
        renderFramePyGame(engine = self)
        renderFramePlt(engine = self)
        #time.sleep(0.1)

    # def close(self):

    def goToLoc(self, walker, locType):
        self.shiftQueue.append((walker, locType))

    def commitShift(self):
        for elem in self.shiftQueue:
            locType = elem[1]
            walker = elem[0]

            if (locType == ls.HOME):
                self.walker_pool.exit(walker)
                self.walker_pool.enter(walker, walker.home)
            elif (locType == ls.WORKPLACE):            
                self.walker_pool.exit(walker)
                self.walker_pool.enter(walker, walker.workPlace)
                salary = walker.workPlace.getSalary()
                walker.home.money += salary
            elif (locType == ls.SCHOOL):
                self.walker_pool.exit(walker)
                self.walker_pool.enter(walker, walker.school)
            elif (locType == ls.LEISURE):
                target = random.randint(0, len(self.locs[ls.LEISURE]) -1)
                self.walker_pool.exit(walker)
                self.walker_pool.enter(walker, self.locs[ls.LEISURE][target])
                
            elif (locType == ls.GROCERIES_STORE):
                target = random.randint(0, len(self.locs[ls.GROCERIES_STORE])-1)
                self.walker_pool.exit(walker)
                self.walker_pool.enter(walker, self.locs[ls.GROCERIES_STORE][target])
                #print("Ora sono a" , walker.loc)
                food = walker.home.family_qty * random.randint(3, 7)
                walker.home.money -= walker.loc.buyFood(food)
                walker.home.bringFood(food)

        self.shiftQueue = []


    def isDone(self, st):
        if st[stats.I]==0 or self.walker_pool.getWalkerNum() == 0: #se tutti muoiono, o il virus si ferma, ridà true
            return True
        else:
            return False