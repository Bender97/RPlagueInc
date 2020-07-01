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

import parameters as param

import engine.schedules.schedules as schedules

class EngineEnv(gym.Env):
    """
    Description:
        A region contains several locations, which contains walkers.
        The engine simulates the infection in this region. Each day is represented as
        a step(). Each step run several update() of each location
    Definitions:
        Num	Function                Symbol      Min     Max
        0	Susceptibles            s(n)        0       POP_NUM
        1   Infected                i(n)        0       POP_NUM
        2   Recovered               r(n)        0       POP_NUM
        3   Deads                   d(n)        0       POP_NUM
        4   Discontent              D(n)        0       Dmax
        5   Population Money Avg    M(n)        0       Mmax
    Other definitions:
        Functions   Meaning
        h(n)        healty walkers: h(n) = s(n) + r(n)
        [Delta i](n)  difference in infected: delta i(n) = i(n) - i(n-1)
    Observations:
        Type: Box(5)
        Num	Observation                 Symbol              Min     Max
        0	Healthy         (norm)      h_n(n)              0       1
        1   Delta infected  (norm)      [Delta_i]_n(n)      -1      1
        2   Average money   (norm)      M_n(n)              0       1
        3   Discontent      (norm)      D_n(n)              0       1
        4   Deads           (norm)      d_n(n)              0       1
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
        Reward = alpha h_n(n) + beta [Delta i]_n(n) + gamma M_n(n) + delta D_n(n) + epsilon d_n(n)
        Note: the normalized versions of the functions are used
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
        'video.frames_per_second': param.FPS                       
    }

    # TODO
    def __init__(self):

        self.RENDER_ALL_DAILY    = 0
        self.RENDER_ALL_HOUR     = 1
        #RENDER_PLT_DAILY    = 2 #not implemented
        #RENDER_PLT_HOUR     = 3 #not implemented
        #RENDER_PYGAME_DAILY = 4 #not implemented
        #RENDER_PYGAME_HOUR  = 5 #not implemented

        self.nLocation = None
        self.nHouses = None

        high = np.array([1.,  1., 1., 1., 1.], dtype=np.float32)
        low = np.array( [0., -1., 0., 0., 0.], dtype=np.float32)

        self.action_space = spaces.Discrete(choices.N_CHOICES*2-1)      # -1 for the NOOP (no counterpart)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        return

    def initialize(self, virus, nHouses, render = None):
        
        self.nHouses = nHouses
        #if (self.nHouses == None):
        #    print("error: nHouses is None. Have you called reset() before calling initialize()?")
        #    exit(1)

        self.virus = virus

        self.shiftQueue = []
        if (render == None):
            self.renderMode = self.RENDER_ALL_DAILY
        else:
            self.renderMode = render


    # end __init__
    ##################################################################

    def computeReward(self, action_applied = False):
        statistics = stats.computeStatistics(self)

        # get base parameters
        s = statistics[stats.S]
        i = statistics[stats.I]
        r = statistics[stats.R]
        d = statistics[stats.D]
        M = statistics[stats.M]
        D = self.discontent
        
        # compute number of healty walkers
        h = s + r
        # compute derivative of infected walkers
        delta_i = i - self.yesterday_infected
        self.yesterday_infected = i

        # compute max discontent
        discontent_max = (param.FOOD_DAILY_DISCONTENT + param.LEISURE_DAILY_DISCONTENT) * self.max_pop + choices.getMaxChoicesDiscontent()
        money_max = self.nHouses * param.MAX_MONEY_PER_HOUSE

        # define functions
        def parametric_relu(x, w):
            return x if x > 0 else w*x

        # compute normalized functions
        h_n = h / self.max_pop
        delta_i_n = parametric_relu(delta_i / self.max_pop, param.RELU_PARAM)
        M_n = M / money_max
        D_n = D / discontent_max
        d_n = d / self.max_pop

        self.observations = [h_n, delta_i_n, M_n, D_n, d_n]

        # compute reward
        reward = param.ALPHA * h_n + param.BETA * delta_i_n + param.GAMMA * M_n + param.DELTA * D_n + param.EPSILON * d_n

        # add action done penalty
        if action_applied:
            reward += param.ZETA

        self.reward = reward

        exist_recovered=False
        for w in self.walker_pool.walker_list:
            if w.isRecovered():
                exist_recovered= True
                break
        if(exist_recovered):
            finished = self.isDone()
        else:
            finished = False

        return self.observations, reward, finished, {}



    def step(self, action):

        ch_applied = False

        if action==0:
            ch_applied = choices.makeChoice(choices.ENACT, choices.CH_NOOP, self)
        elif action >= 7:
            ch_applied = choices.makeChoice(choices.ABOLISH, action-6, self)
        else:
            ch_applied = choices.makeChoice(choices.ENACT, action, self)

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

        # update discontent for food and daily
        for loc in self.locs[ls.HOME]:
            if not loc.needFood():
                loc.eatFood()
            else:
                self.discontent += param.FOOD_DAILY_DISCONTENT
        
        self.discontent += self.daily_discontent


        # try virus events
        start_inf = time.time()

        for locList in self.locs:
            for loc in locList:  # produce the deaths. tryInfection and tryDisease are called inside location file                
                for w in loc.walkers[param.INCUBATION]:
                    self.virus.tryDisease(w, self)
                for w in loc.walkers[param.ASYMPTOMATIC]:
                    self.virus.tryRecovery(w, self)
                for w in loc.walkers[param.INFECTED]:
                    self.virus.tryDeath(w, self)

        end_inf = time.time()
        #print("time elapsed for infection is:" + str(end_inf - start_inf))


        ######### reward calculation #########

        return_values = self.computeReward(ch_applied)

        # update step values
        self.steps_done +=1
        self.discontent = 0

        return return_values


    def reset(self):

        # simulation dependent variables
        self.steps_done = 0
        self.walker_pool = WalkerPool()
        self.locs = [[], [], [], [], []]
        self.choice_str = None
        self.observations = [0, 0, 0, 0, 0]
        self.reward = 0

        reggen.regionGen(self)

        popgen.genPopulation(self)


        # choices dependent variables
        self.closed_locs = []
        self.quarantine = []
        self.safe_dist = 0

        choices.setupChoices(self)
        
        # reward dependent variables
        self.discontent = 0
        self.daily_discontent = 0
        self.yesterday_infected = 0
        self.deads = 0

        # for pygame rendering
        self.screen = None
        self.fps = 0
        self.paused = False

        # calculate position on screen for each location
        self.locPos = [[], [], [], [], []]
        
        # initialize plots
        self.figs = {}

        initPlt(engine = self,
                figure = 1,
                xlabel = 'days',
                ylabel = 'population',
                n_subplots = 4
                )
        
        initPlt(engine = self,
                figure = 2,
                xlabel = 'days',
                ylabel = 'status',
                n_subplots = 6
                )
        
        initPyGame(self, border=param.BORDER, padding = param.PADDING, name_of_window='Region')

        return self.computeReward()[0]

    def render(self, mode='human'):
        renderFramePyGame(engine = self)

        statistics_dict = stats.computeStatistics(self)

        to_graph = [stats.S, stats.I, stats.R, stats.D]
        statistics = [statistics_dict[k] for k in to_graph]

        renderFramePlt(engine = self,
                       figure = 1,
                       new_xdata = self.steps_done,
                       new_ydata = statistics,
                       labels = (   
                            'susceptibles + asymptomatics + incubation: '+ str(statistics[0]),
                            'infected (disease): '                       + str(statistics[1]),
                            'recovered: '                                + str(statistics[2]),
                            'dead: '                                     + str(statistics[3])
                            )
                       )

        # scale the observations to compose the graphs
        statuses = self.observations.copy()
        statuses[0] *= param.ALPHA
        statuses[1] *= param.BETA
        statuses[2] *= param.GAMMA
        statuses[3] *= param.DELTA
        statuses[4] *= param.EPSILON
        statuses.append(self.reward)
        
        renderFramePlt(engine = self,
                       figure = 2,
                       new_xdata = self.steps_done,
                       new_ydata = statuses,
                       labels = (
                            'h_n: '        + str("{:.2f}".format(statuses[0])),
                            'delta_i_n: '  + str("{:.2f}".format(statuses[1])),
                            'M_n: '        + str("{:.2f}".format(statuses[2])),
                            'D_n: '        + str("{:.2f}".format(statuses[3])),
                            'd_n: '        + str("{:.2f}".format(statuses[4])),
                            'reward: '     + str("{:.2f}".format(statuses[5]))
                            )
                       )
        
        self.choice_str = None
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
                walker.home.bringMoney(salary)
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
                if (walker.home.money >= walker.loc.buyFood(food)):
                    walker.home.money -= walker.loc.buyFood(food)
                    walker.home.bringFood(food)

        self.shiftQueue = []


    def isDone(self):
        return not stats.isThereAnyInfected(self)