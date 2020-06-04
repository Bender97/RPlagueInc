import pygame
import sys
import random
import math

import numpy as np

import time

from walkers.Walker import Walker
import walkers.healthState as h

BLACK = (0, 0, 0)

color = [
    (255, 255, 255),  # WHITE - SUSCEPTIBLE
    (0, 0, 255),  # LIGHTGREY - INCUBATION
    (255, 50, 50),  # RED - INFECTED
    (255, 255, 0),  # YELLOW - ASYMPTOMATIC
    (50, 255, 50),  # GREEN - RECOVERED
    BLACK  # BLACK - DEAD
]


class Location:
    '''
    Attributes
    ----------
    size_x : integer
    size_y : integer
    max_capacity : integer
    walkers : vector of Walkers
    distance_list : vector of pairs of Walkers
    '''

    def __init__(self, size_x, size_y, max_capacity):

        self.size_x = size_x
        self.size_y = size_y
        self.max_capacity = max_capacity

        self.walkers = []
        for i in range(h.statusNum):
            self.walkers.append([])

        # variables for rendering
        self.screen = None
        self.fps = 0
        self.paused = False

    # end __init__

    def initRendering(self):
        '''
        Init the rendering engine
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('Region')
        self.fps = pygame.time.Clock()
        self.paused = False

    def render(self, virus):
        '''
        render the current situation
        Parameters
        ----------
        virus: Virus
            the virus spreading
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
        if not self.paused:
            self.screen.fill(BLACK)

            font = pygame.font.Font(None, 36)

            for walkerStatus in range(h.statusNum):
                for walker in self.walkers[walkerStatus]:
                    pygame.draw.circle(self.screen, color[walker.status], (walker.x, walker.y), 5, 0)
                    pygame.draw.circle(self.screen, color[walker.status], (walker.x, walker.y), int(virus.range / 2), 1)

            pygame.display.update()
            self.fps.tick(30)


# end class Location

def run1HOUR(engine):
    '''
    update the context inside the location ( a minute (or second, must decide) of life , for each update call)
    1) update positions
    2) tryInfection()
    Parameters
    ----------
    virus: Virus
        the virus spreading
    '''

    coord_array = np.array(engine.walker_pool.coord_list, dtype = float)
    sizes = np.array([[w.loc.size_x - 1, w.loc.size_y - 1] for w in engine.walker_pool.walker_list])

    walker_num = engine.walker_pool.getWalkerNum()

    diameter = 8

    np_time = 0
    dist_time = 0

    for _ in range(60):
            
        # 1) update positions
    
        start = time.time()

        # compute a random walk
        walks = (np.random.random((walker_num, 2)) - 0.5) * diameter

        # make the walk
        coord_array += walks

        # limit the walk inside the locations
        np.clip(coord_array, 0, sizes, out = coord_array)

        end = time.time()

        np_time += end - start

        # 2) tryInfection()
        # CHECK FOR EACH WALKER IF IT's CLOSE TO AN INFECTED
        #   IF SO -> ROLL the DICE

        start = time.time()

        for locList in engine.locs:
            for loc in locList:

                for susceptible in loc.walkers[h.SUSCEPTIBLE]:
                    flag = 0    # will hold the period of incubation, if infection happens

                    for asymptomatic in loc.walkers[h.ASYMPTOMATIC]:
                        if (distance(coord_array, susceptible, asymptomatic) < engine.virus.range):
                            flag = engine.virus.tryInfection(susceptible)
                            if (flag):
                                break  # non ha senso fare altri controlli
                    if not flag:
                        for infected in loc.walkers[h.INFECTED]:
                            if (distance(coord_array, susceptible, infected) < engine.virus.range):
                                flag = engine.virus.tryInfection(susceptible)
                                if (flag):
                                    susceptible.infectedBy = infected
                                    break  # non ha senso fare altri controlli
                    if flag:
                        susceptible.updateVirusTimer(value=flag)
                        loc.walkers[h.SUSCEPTIBLE].remove(susceptible)
                        loc.walkers[h.INCUBATION].append(susceptible)

        end = time.time()

        dist_time += end - start
    #end for

    engine.walker_pool.coord_list = coord_array.tolist()

    print ("time for numpy: " + str(np_time))
    print ("time for dist: " + str(dist_time))

# end update


def distance(coord_list, walker1, walker2):

    w1_x = coord_list[walker1.index][0]
    w1_y = coord_list[walker1.index][1]
    w2_x = coord_list[walker2.index][0]
    w2_y = coord_list[walker2.index][1]

    return math.sqrt((w2_x - w1_x) ** 2 + (w2_y - w1_y) ** 2)
# end distance