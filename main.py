from structures.locations import *
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

import time

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)

loc = buildDefaultLocation(HOME)
loc.initRendering()

for i in range(10):
    walker = Walker(640, 480, random.randint(1, 100), 1, loc)
    
    if (random.random()<0.2):
        walker.setStatus(h.INCUBATION)
        walker.updateVirusTimer(random.randint(2, 14))

    loc.enter(walker)

while(True):
    for _ in range(24):
        loc.run1HOUR(virus)

        for incubated in loc.walkers[h.INCUBATION]:
            if (incubated.getVirusTimer()>0):
                incubated.updateVirusTimer()
        
        for asymptomatic in loc.walkers[h.ASYMPTOMATIC]:
            if (asymptomatic.getVirusTimer()>0):
                asymptomatic.updateVirusTimer()
        
        loc.render(virus)
        time.sleep(0.5)