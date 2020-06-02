import structures.locations as ls
from engine.schedules.activity import Activity, Fork, Branch
import engine.schedules.probabilities as prob
import random

'''
Ages;
    - Child
    - Adult
    - Elderly
'''

# Ages
CHILD = 0
ADULT = 1
ELDERLY = 2

# Hours
MIN_HOUR = 0
MAX_HOUR = 23

# Activities
A_STAY_HOME = 0
A_WORK = 1
A_FUN = 2
A_SCHOOL = 3
A_GROCERIES = 4

# Flags
F_IF_NEED_FOOD = 1
F_IF_NOT_NEED_FOOD = -1

# Data indexes
WALKER = 0
HOUR = 1


SCHEDULES = {
    CHILD : [
        Activity(MIN_HOUR, 7, A_STAY_HOME),
        Fork(8, 15, [
            Branch(prob.forSure, activities = [
                Activity(8, 15, A_SCHOOL),
                ]),
            Branch(prob.uniformChoice, 0.75, activities = [
                Activity(8, 15, A_FUN),
                ])
            ]),
        Fork(16, 19, [
            Branch(prob.uniformChoice, 0.6, flags = [F_IF_NOT_NEED_FOOD], activities = [
                Activity(16, 19, A_FUN)
                ]),
            Branch(prob.forSure, flags = [F_IF_NEED_FOOD], activities = [
                Activity(16, 19, A_GROCERIES)
                ])
            ]),
        Activity(20, MAX_HOUR, A_STAY_HOME),
        ],
    
    ADULT : [
        Activity(MIN_HOUR, 7, A_STAY_HOME),
        Fork(8, 18, [
            Branch(prob.forSure, activities = [
                Activity(8, 18, A_WORK),
                ]),
            Branch(prob.forSure, activities = [
                Fork(8, 11, [
                    Branch(prob.adultHomeProbFcn, flags = [F_IF_NEED_FOOD], activities = [
                        Activity(8, 11, A_GROCERIES),
                        ])
                    ]),
                Activity(12, 15, A_STAY_HOME),
                Fork(15, 18, [
                    Branch(prob.forSure, flags = [F_IF_NEED_FOOD], activities = [
                        Activity(15, 18, A_GROCERIES),
                        ])
                    ])
                ])
            
            ]),
        Activity(19, 21, A_STAY_HOME),
        Fork(22, MAX_HOUR, [
            Branch(prob.uniformChoice, 0.7, activities = [
                Activity(22, MAX_HOUR, A_FUN),
                ])
            ])
        ],

    ELDERLY : [
        Activity(MIN_HOUR, 13, A_STAY_HOME),
        Fork(14, 19, [
            Branch(prob.forSure, flags = [F_IF_NEED_FOOD], activities = [
                Activity(14, 16, A_GROCERIES),
                Activity(17, 19, A_STAY_HOME)
                ]),
            Branch(prob.uniformChoice, 0.5, activities = [
                Activity(14, 19, A_FUN)
                ])
            ]),
        Activity(19, MAX_HOUR, A_STAY_HOME)
        ]

    }


def applySchedule(engine, walker, hour):
    age = 0
    if walker.isChild():
        #print("Child ")
        age = CHILD
    elif walker.isAdult():
        #print("Adult ")
        age = ADULT
    elif walker.isElder():
        #print("Elderly ")
        age = ELDERLY

    # get the correct schedule by age
    schedule = SCHEDULES[age]
    # do the right activity by schedule
    doActivities(engine, walker, schedule, hour)
# end applySchedule

def doActivities (engine, walker, schedule, hour):
    for act in schedule:
        # if the hour is in the activity then do it and exit
        if act.contains(hour):
            # if it's an activity do it
            if isinstance(act, Activity):
                doAct(engine, act, walker)
            # if it's a fork, parse it
            if isinstance(act, Fork):
                tryBranches(engine, act, walker, hour)
            return



# end doActivities

def doAct (engine, act, walker):

    activity = act.activity
    # switch the activity type
    if activity == A_GROCERIES:
        if not walker.wentForGroceries:
            walker.wentForGroceries = True
            #print("Sto andando a comprare cibo")
            engine.goToLoc(walker, ls.GROCERIES_STORE)
            
    else:
        walker.wentForGroceries = False
        if activity == A_STAY_HOME:
            #print("Staying home")
            if not walker.loc.type == ls.HOME:
                engine.goToLoc(walker, ls.HOME)
        elif activity == A_FUN:
            #print("Having fun")
            if not walker.loc.type == ls.LEISURE:
                if ls.LEISURE in engine.closed_locs:
                    engine.goToLoc(walker, ls.HOME)
                    engine.discontent += 10
                else:
                    engine.goToLoc(walker, ls.LEISURE)
        elif activity == A_WORK:
            #print("Working")
            if not walker.loc.type == ls.WORKPLACE:
                if ls.WORKPLACE in engine.closed_locs:
                    engine.goToLoc(walker, ls.HOME)
                    engine.discontent += 10
                else:
                    engine.goToLoc(walker, ls.WORKPLACE)
        elif activity == A_SCHOOL:
            #print("Going to school")
            if not walker.loc.type == ls.SCHOOL:
                if ls.SCHOOL in engine.closed_locs:
                    engine.goToLoc(walker, ls.HOME)
                    engine.discontent += 10
                else:
                    engine.goToLoc(walker, ls.SCHOOL)
# end doAct

def tryBranches (engine, fork, walker, hour):
    branches = fork.branches
    # try each branch until one works
    for br in branches:

        data = {WALKER : walker, HOUR : hour}
        # try the random choice and the condition flags
        if br.tryChoice(data) and tryFlags(engine, br, walker):
            doActivities(engine, walker, br.activities, hour)
            return
    
    # if no branch works, stay at home
    doAct(engine, Activity(fork.start, fork.end, A_STAY_HOME), walker)
# end tryBranches

def tryFlags (engine, branch, walker):

    flags = branch.flags
    result = True

    for f in flags:
        if f == F_IF_NEED_FOOD:
            result = result and walker.home.needFood()
        if f == F_IF_NOT_NEED_FOOD:
            result = result and not walker.home.needFood()

    return result
# end tryFlags

