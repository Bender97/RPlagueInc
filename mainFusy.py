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
                    
    walker = Walker( 640, # loc_width
                     480, # loc_height
                     random.randint(1, 100), # age
                     1,   # disobedience
                     loc, # where it lives
                     None)
    
    if (random.random()<0.2):
        walker.setStatus(h.INCUBATION)
        walker.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))

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

        for infected in loc.walkers[h.INFECTED]:
            if (infected.getVirusTimer()>0):
                infected.updateVirusTimer()
            else:
                flag = virus.tryDeath(infected)

                loc.walkers[h.INFECTED].remove(infected)

                if (flag):
                    loc.walkers[h.DEAD].append(infected)
                    print("+1 DEAD")
                else:
                    loc.walkers[h.RECOVERED].append(infected)
        
        loc.render(virus)
        time.sleep(0.5)