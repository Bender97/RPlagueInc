import random
import parameters as param
from walkers.Walker import Walker
import structures.locations as ls

def genPopulation(env):

    num_child = -1
    num_adult = -1
    num_elder = -1

    env.max_pop = 0

    for home in env.locs[ls.HOME]:

        maxPeople = home.max_capacity
        generatedPeople = random.randint(1, maxPeople)
        env.max_pop += generatedPeople

        for _ in range(generatedPeople):

            age = random.randint(1, 100)

            if age>param.old_age:
                num_elder += 1
                dutyPlace = None
            elif age < param.young_age:
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

    to_infect = random.sample(env.walker_pool.walker_list, param.INITIAL_CASES)
    for w in to_infect:
        env.walker_pool.exit(w)
        w.setStatus(param.INCUBATION)
        w.updateVirusTimer(value = random.randint(param.INCUBATION_DURATION_RANGE[0], param.INCUBATION_DURATION_RANGE[1]))
        env.walker_pool.enter(w, w.home)
    ################# end

    print(str(num_child + num_adult + num_elder) + " people have been generated")