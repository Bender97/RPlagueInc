import random
import walkers.healthState as h
from walkers.Walker import Walker
import structures.locations as ls

def genPopulation(env):

    num_child = -1
    num_adult = -1
    num_elder = -1

    for home in env.locs[ls.HOME]:

        maxPeople = home.max_capacity
        generatedPeople = random.randint(1, maxPeople)

        for _ in range(generatedPeople):

            age = random.randint(1, 100)

            if age>h.old_age:
                num_elder += 1
                dutyPlace = None
            elif age < h.young_age:
                num_child += 1
                dutyPlace = env.locs[ls.SCHOOL][num_child % len(env.locs[ls.SCHOOL])]
            else:
                num_adult += 1
                dutyPlace = env.locs[ls.WORKPLACE][num_adult % len(env.locs[ls.WORKPLACE])]

            w = Walker( home.size_x, 
                        home.size_y, 
                        age, 
                        random.random(), 
                        home, 
                        dutyPlace
                        )

            ################# generate INFECTED (only INCUBATION)

            if (random.random()<0.2):
                w.setStatus(h.INCUBATION)
                w.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))
            
            ################# end

            w.enter(w.home)



    print(str(num_child + num_adult + num_elder) + " people have been generated")