import random
import walkers.healthState as h
from walkers.Walker import Walker
import structures.locations as ls

def genPopulation(env):

    num_people = 0

    for home in env.locs[ls.HOME]:

        maxPeople = home.max_capacity
        generatedPeople = random.randint(1, maxPeople)

        for i in range(generatedPeople):

            w = Walker(home.size_x, 
                        home.size_y, 
                        random.randint(1, 100), 
                        random.random(), 
                        home, 
                        env.locs[ls.SCHOOL][num_people % len(env.locs[ls.SCHOOL])],
                        env.locs[ls.WORKPLACE][num_people % len(env.locs[ls.WORKPLACE])]
                        )
            
            ################# generate INFECTED (only INCUBATION)

            if (random.random()<0.2):
                w.setStatus(h.INCUBATION)
                w.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))
            
            ################# end

            home.enter(w)

            num_people += 1