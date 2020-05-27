from Virus import Virus
from location import Location
from Walker import Walker

import healthState as h

virus = Virus(range = 40, pInfection = 1	, healthParams = 1, healingParams = 1)

loc = Location(640, 480, 20)
loc.initRendering()

for i in range(20):
	loc.enter(Walker(640, 480, 18, 1))

# HARDCODED
loc.walkers[0].setStatus(h.INFECTED)
loc.no_infected = 1
while(True):
	loc.update(virus)
	print(loc.no_infected)
	loc.render(virus)