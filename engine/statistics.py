from structures.location import Location
from structures.locations import Home
import walkers.healthState as h
import networkx as nx

'''

R0:
    The average number of secondary infections produced when one infected individual
    is introduced into a host population where everyone is susceptible.
    If R0 is greater than one then the outbreak will lead to an epidemic, and if R0
    is less than one then the outbreak will become extinct

'''

S = 0   # Susceptibles
I = 1   # Infected
R = 2   # Recovered
D = 3   # Deads
R0 = 4  # Avg number of secondary infections produced by one infected individual
M = 5   # Money


def computeStatistics(engine):

    statistics = {
        S: 0,
        I: 0,
        R: 0,
        D: engine.deads,
        R0: 0,
        M: 0
    }


    money_accum = 0
    n_homes = 0
    # for each location in the region compute the SIR statistics + M

    for locList in engine.locs:
        for loc in locList:
            statistics[S] += len(loc.walkers[h.SUSCEPTIBLE]) + len(loc.walkers[h.ASYMPTOMATIC]) + len(loc.walkers[h.INCUBATION])
            statistics[I] += len(loc.walkers[h.INFECTED])
            statistics[R] += len(loc.walkers[h.RECOVERED_FROM_INFECTED])
            if isinstance(loc, Home):
                money_accum += loc.money
                n_homes += 1
    # end for
    statistics[M] = money_accum / n_homes

    # find from the contact list the avg number of secondary infection (R0)
    secondary_inf_accum = 0
    for w in engine.contact_list:
        secondary_inf_accum += engine.contact_list[w]
    # end for

    length = len(engine.contact_list)
    if (length):
        #print(engine.contact_list)
        statistics[R0] = secondary_inf_accum / len(engine.contact_list)


    return statistics

# end computeStatistics