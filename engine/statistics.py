from structures.location import Location
import structures.locations as ls
import parameters as param
import networkx as nx


S = 0   # Susceptibles
I = 1   # Infected
R = 2   # Recovered
D = 3   # Deads
M = 4   # Money

def computeStatistics(engine):

    statistics = {
        S: 0,
        I: 0,
        R: 0,
        D: engine.deads,
        M: 0
    }

    money_accum = 0
    n_homes = 0
    # for each location in the region compute the SIR statistics + M

    for locList in engine.locs:
        for loc in locList:
            statistics[S] += len(loc.walkers[param.SUSCEPTIBLE]) + len(loc.walkers[param.ASYMPTOMATIC]) + len(loc.walkers[param.INCUBATION]) + len(loc.walkers[param.RECOVERED_FROM_ASYMPTOMATIC])
            statistics[I] += len(loc.walkers[param.INFECTED])
            statistics[R] += len(loc.walkers[param.RECOVERED_FROM_INFECTED])
            if loc.type == ls.HOME:
                money_accum += loc.money
                n_homes += 1
    # end for
    statistics[M] = money_accum / n_homes


    return statistics

# end computeStatistics

def isThereAnyInfected(engine):
    for locList in engine.locs:
        for loc in locList:
            infected = len(loc.walkers[param.INFECTED]) + len(loc.walkers[param.ASYMPTOMATIC]) + len(loc.walkers[param.INCUBATION])
            if infected > 0:
                return True
        # end for
    # end for
    return False