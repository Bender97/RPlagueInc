import random
import walkers.healthState as h
from walkers.Walker import Walker
import structures.locations as ls

INITIAL_CASES = 2

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

            w = Walker( age, 
                        random.random(), #disobedience
                        home, 
                        dutyPlace
                        )

            env.walker_pool.add(w)
            env.walker_pool.enter(w, w.home)

    ################# generate INFECTED (only INCUBATION)

    to_infect = random.sample(env.walker_pool.walker_list, INITIAL_CASES)
    for w in to_infect:
        env.walker_pool.exit(w)
        w.setStatus(h.INCUBATION)
        w.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))
        env.walker_pool.enter(w, w.home)
    ################# end

    print(str(num_child + num_adult + num_elder) + " people have been generated")