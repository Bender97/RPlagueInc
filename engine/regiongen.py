import networkx as nx
import random
import numpy as np
import walkers.healthState
import structures.locations as l
import matplotlib.pyplot as plt

P_HOME = 0.24
P_OTHER = (1 - P_HOME) / 4.0

MIN_DEGREE = 4
MAX_DEGREE = 9


def regionGen(nLocations):
    degreeSeq=[]
    seqSum=0
    dict = {} #dict that associates node IDs to type of location(costants). Used for labeling in drawing
    ObjDict={} #dict that associates node IDs to istances of locations Classes
    for i in range(0,nLocations-1):
        temp = random.randint(MIN_DEGREE, MAX_DEGREE)
        degreeSeq.append(temp)
        seqSum += temp
        dict[i] = np.random.choice([l.HOME, l.WORKPLACE, l.GROCERIES_STORE, l.SCHOOL, l.LEISURE], 1, p=[P_HOME, P_OTHER, P_OTHER, P_OTHER, P_OTHER])[0]
        if dict[i]==l.HOME:
            ObjDict[i]=l.buildDefaultHome()
        elif dict[i]==l.WORKPLACE:
            ObjDict[i] = l.buildDefaultWorkplace()
        elif dict[i]==l.GROCERIES_STORE:
            ObjDict[i] = l.buildDefaultStore()
        elif dict[i]==l.SCHOOL:
            ObjDict[i] = l.buildDefaultSchool()
        else:
            ObjDict[i] = l.buildDefaultLeisure()
    temp = 0
    while (seqSum + temp)%2 !=0:
        temp = random.randint(4, 9)
    degreeSeq.append(temp)
    seqSum += temp
    dict[nLocations-1] = np.random.choice([l.HOME, l.WORKPLACE, l.GROCERIES_STORE, l.SCHOOL, l.LEISURE], 1,p=[P_HOME, P_OTHER, P_OTHER, P_OTHER, P_OTHER])[0]
    if dict[nLocations-1] == l.HOME:
        ObjDict[nLocations-1] = l.buildDefaultHome()
    elif dict[nLocations-1] == l.WORKPLACE:
        ObjDict[nLocations-1] = l.buildDefaultWorkplace()
    elif dict[nLocations-1] == l.GROCERIES_STORE:
        ObjDict[nLocations-1] = l.buildDefaultStore()
    elif dict[nLocations-1] == l.SCHOOL:
        ObjDict[nLocations-1] = l.buildDefaultSchool()
    else:
        ObjDict[nLocations-1] = l.buildDefaultLeisure()
    G = nx.configuration_model(degreeSeq)
    nx.set_node_attributes(G,ObjDict,"LocType")

    return G