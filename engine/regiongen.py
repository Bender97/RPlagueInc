import networkx as nx
import random
import numpy as np
import structures.locations as l
import matplotlib.pyplot as plt

P_HOME = 0.25
P_GROCERIES=0.22
P_OTHER = (1 - (P_HOME + P_GROCERIES)) / 3.0

MIN_DEGREE = 9
MAX_DEGREE = 15


def regionGen(nLocations):
    degreeSeq=[]
    seqSum=0
    dict = {} #dict that associates node IDs to type of location(costants). Used for labeling in drawing
    ObjDict={} #dict that associates node IDs to istances of locations Classes
    nL =[0 ,0, 0, 0, 0]


    for i in range(0,nLocations-1):
        temp = random.randint(MIN_DEGREE, MAX_DEGREE)
        degreeSeq.append(temp)
        seqSum += temp
        dict[i] = np.random.choice([l.HOME, l.WORKPLACE, l.GROCERIES_STORE, l.SCHOOL, l.LEISURE], 1, p=[P_HOME, P_OTHER, P_GROCERIES, P_OTHER, P_OTHER])[0]
        if dict[i]==l.HOME:
            ObjDict[i]=l.buildDefaultHome()
            nL[l.HOME]+=1
        elif dict[i]==l.WORKPLACE:
            ObjDict[i] = l.buildDefaultWorkplace()
            nL[l.WORKPLACE] += 1
        elif dict[i]==l.GROCERIES_STORE:
            ObjDict[i] = l.buildDefaultStore()
            nL[l.GROCERIES_STORE] += 1
        elif dict[i]==l.SCHOOL:
            ObjDict[i] = l.buildDefaultSchool()
            nL[l.SCHOOL] += 1
        else:
            ObjDict[i] = l.buildDefaultLeisure()
            nL[l.LEISURE] += 1
    temp = 0
    while (seqSum + temp)%2 !=0:
        temp = random.randint(MIN_DEGREE, MAX_DEGREE)
    degreeSeq.append(temp)
    seqSum += temp
    dict[nLocations-1] = np.random.choice([l.HOME, l.WORKPLACE, l.GROCERIES_STORE, l.SCHOOL, l.LEISURE], 1,p=[P_HOME, P_OTHER, P_GROCERIES, P_OTHER, P_OTHER])[0]
    if dict[nLocations-1] == l.HOME:
        ObjDict[nLocations-1] = l.buildDefaultHome()
        nL[l.HOME] += 1
    elif dict[nLocations-1] == l.WORKPLACE:
        ObjDict[nLocations-1] = l.buildDefaultWorkplace()
        nL[l.WORKPLACE] += 1
    elif dict[nLocations-1] == l.GROCERIES_STORE:
        ObjDict[nLocations-1] = l.buildDefaultStore()
        nL[l.GROCERIES_STORE] += 1
    elif dict[nLocations-1] == l.SCHOOL:
        ObjDict[nLocations-1] = l.buildDefaultSchool()
        nL[l.SCHOOL] += 1
    else:
        ObjDict[nLocations-1] = l.buildDefaultLeisure()
        nL[l.LEISURE] += 1
    G = nx.configuration_model(degreeSeq)
    nx.set_node_attributes(G,ObjDict,"LocType")
    print("Created a city with",nL[l.HOME],"homes,",nL[l.WORKPLACE],"workplaces,",nL[l.GROCERIES_STORE],"groceries,",nL[l.SCHOOL],"schools and",nL[l.LEISURE],"leisures")

    return G