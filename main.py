from structures.locations import *
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)

loc = buildDefaultLocation(HOME)
loc.initRendering()

for i in range(50):
    walker = Walker(640, 480, random.randint(1, 100), 1, loc)
    
    if (random.random()<0.2):
    	walker.setStatus(h.INCUBATION)

    loc.enter(walker)

# HARDCODED

inf = loc.walkers[h.SUSCEPTIBLE][0]

inf.setStatus(h.INFECTED)

loc.walkers[h.SUSCEPTIBLE].remove(inf)
loc.walkers[h.INFECTED].append(inf)

loc.no_infected = 1
while(True):
    loc.update(virus)
    #print(loc.no_infected)
    loc.render(virus)
