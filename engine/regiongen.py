import random
import structures.locations as ls
import math
def regionGen(env):
    '''
    35 case
    5 scuole
    5 divertimento
    5 supermercati
    5 lavoro
    
    rapporto case altri luoghi:
    10 a 1
    '''
    env.nLocation = 0

    for i in range(env.nHouses):
        env.locs[ls.HOME].append(ls.buildDefaultHome())
    env.nLocation+=env.nHouses

    for i in range(math.ceil(env.nHouses/10)):

        env.locs[ls.WORKPLACE].append(ls.buildDefaultWorkplace())
        env.locs[ls.LEISURE].append(ls.buildDefaultLeisure())
        env.locs[ls.SCHOOL].append(ls.buildDefaultSchool())
        env.locs[ls.GROCERIES_STORE].append(ls.buildDefaultStore())
        
        env.nLocation+=4