from structures.locations import *
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)

loc = buildDefaultLocation(HOME)
loc.initRendering()

for i in range(20):
    walker = Walker(640, 480, random.randint(1, 100), 1, loc)
    
    if (random.random()<0.2):
    	walker.setStatus(h.INCUBATION)
    	walker.updateVirusTimer(random.randint(2, 14))

    loc.enter(walker)


while(True):
    loc.update(virus)
    loc.render(virus)