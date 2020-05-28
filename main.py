from structures.locations import *
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)

loc = buildDefaultLocation(HOME)
loc.initRendering()

for i in range(20):
    loc.enter(Walker(640, 480, 18, 1, loc))

# HARDCODED
loc.walkers[0].setStatus(h.INFECTED)
loc.no_infected = 1
while(True):
    loc.update(virus)
    print(loc.no_infected)
    loc.render(virus)
