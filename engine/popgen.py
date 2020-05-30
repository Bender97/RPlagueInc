import networkx as nx
import random
import numpy as np
import walkers.healthState as h
from walkers.Walker import Walker
import structures.locations as l

def genPopulation(region):
    try:
        Gdict = nx.get_node_attributes(region, 'LocType')
    except:
        print("No region graph has been set")
    for key in Gdict.keys():
        if isinstance(Gdict[key], l.Home):
            maxPeople = Gdict[key].max_capacity
            generatedPeople = random.randint(1, maxPeople)
            for i in range(0, generatedPeople):
                w = Walker(Gdict[key].size_x, Gdict[key].size_y, random.randint(1, 100), random.random(), Gdict[key], key)
                
                ##############àààà RIGHE AGGIUNTE PER DIVERTIMENTO - da cancellare

                if (random.random()<0.2):
                    w.setStatus(h.INCUBATION)
                    w.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))
                
                ##############àààà end

                Gdict[key].enter(w)
