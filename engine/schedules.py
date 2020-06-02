import random
import structures.locations as ls

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
            Branch(forSure, activities = [
                Activity(8, 15, A_SCHOOL),
                ]),
            Branch(uniformChoice, 0.75, activities = [
                Activity(8, 15, A_FUN),
                ])
            ]),
        Fork(16, 19, [
            Branch(tryDisobey, flags = [F_IF_NOT_NEED_FOOD], activities = [
                Activity(16, 19, A_FUN)
                ]),
            Branch(forSure, flags = [F_IF_NEED_FOOD], activities = [
                Activity(16, 19, A_GROCERIES)
                ])
            ]),
        Activity(20, MAX_HOUR, A_STAY_HOME),
        ],
    
    ADULT : [
        Activity(MIN_HOUR, 7, A_STAY_HOME),
        Fork(8, 18, [
            Branch(forSure, activities = [
                Activity(8, 18, A_WORK),
                ]),
            Branch(forSure, activities = [
                Fork(8, 11, [
                    Branch(adultHomeProbFcn, flags = [F_IF_NEED_FOOD], activities = [
                        Activity(8, 12, A_GROCERIES),
                        ])
                    ]),
                Activity(12, 15, A_STAY_HOME),
                Fork(15, 18, [
                    Branch(forSure, flags = [F_IF_NEED_FOOD], activities = [
                        Activity(15, 18, A_GROCERIES),
                        ])
                    ])
                ])
            
            ]),
        Activity(19, 21, A_STAY_HOME),
        Fork(22, MAX_HOUR, activities = [
            Branch(tryDisobey, [
                Activity(8, 15, A_FUN),
                ])
            ])
        ],

    ELDERLY : [
        Activity(MIN_HOUR, 13, A_STAY_HOME),
        Fork(14, 19, [
            Branch(forSure, flags = [F_IF_NEED_FOOD], activities = [
                Activity(14, 16, A_GROCERIES),
                Activity(17, 19, A_STAY_HOME)
                ]),
            Branch(tryDisobey, activities = [
                Activity(14, 19, A_FUN)
                ])
            ]),
        Activity(19, MAX_HOUR, A_STAY_HOME)
        ]

    }


def applySchedule(engine, walker, hour):
    age = 0
    if walker.isChild():
        age = CHILD
    elif walker.isAdult():
        age = ADULT
    elif walker.isElder():
        age = ELDERLY

    schedule = SCHEDULES[age]
    doActivities(walker, schedule, hour)
# end applySchedule

def doActivities (engine, walker, schedule, hour):
    for act in schedule:
        # if the hour is in the activity then do it and exit
        if act.contains(hour):
            if isinstance(act, Activity):
                doAct(engine, act, walker)
            if isInstance(act, Fork):
                tryBranches(engine, act, walker, hour)
            return



# end doActivities

def doAct (engine, act, walker):

    activity = act.activity
    # switch the activity type
    if activity == A_GROCERIES:
        if not walker.wentForGroceries:
            self.goHome(w)
            w.wentForGroceries = True
            print("Sto andando a comprare cibo")
            engine.goToNearestLoc(walker, ls.GROCERIES_STORE)
            print("Ora sono a" , engine.gDict[walker.loc])
            food = walker.home.family_qty * random.randint(3, 7)
            walker.home.money -= engine.gDict[walker.loc].buyFood(food)
            walker.home.bringFood(food)
    else:
        w.wentForGroceries = False
        if activity == A_STAY_HOME:
            if not walker.loc != walker.homeNode:
                engine.goHome(walker)
        elif activity == A_FUN:
            if not walker.isInA(engine, ls.Leisure):
                self.goHome(w)
                engine.goToNearestLoc(walker, ls.LEISURE)
        elif activity == A_WORK:
            if not walker.isInA(engine, ls.Workplace):
                self.goHome(w)
                engine.goToNearestLoc(walker, ls.WORKPLACE)
        elif activity == A_SCHOOL:
            if not walker.isInA(engine, ls.School):
                self.goHome(w)
                engine.goToNearestLoc(walker, ls.SCHOOL)
# end doAct

def tryBranches (engine, fork, walker, hour):

    branches = walker.branches
    # try each branch until one works
    for br in branches:

        data = {WALKER : walker, HOUR : hour}
        # try the random choice and the condition flags
        if br.tryChoice(data) and tryFlags(engine, br, walker):
            doActivities(engine, walker, br, hour)
            return
    
    # if no branch works, stay at home
    doAct(engine, Activity(fork.start, fork.end, A_STAY_HOME), walker)
# end tryBranches

def tryFlags (engine, branch, walker):

    flags = branch.flags
    result = True

    for f in flags:
        if f == F_IF_NEED_FOOD:
            result = result and w.home.needFood()
        if f == F_IF_NOT_NEED_FOOD:
            result = result and not w.home.needFood()

    return result
# end tryFlags

class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, hour):
        return self.start <= hour <= self.end

# end Interval

class Activity(Interval):

    def __init__(self, start, end, activity):
        super.__init__(start, end)
        self.activity = activity

# end Activity

class Fork(Interval):

    def __init__(self, start, end, branches):
        super.__init__(start, end)
        self.branches = branches
    
# end Activity

class Branch:

    def __init__(self, prob_funct = forSure, value = 1, flags = [], activities = []):
        self.prob_funct = prob_funct
        self.value = value
        self.flags = flags
        self.activities = activities

    def tryChoice(self, data): #TODO: implement flags
        return self.prob_funct(data, self.value)

# end Branch

# some probability functions
def forSure(data):
    return True

def uniformChoice(data, value):
    return random.random() < value

def tryDisobey(data, value):
    return random.random() < data[WALKER].disobedience

def adultHomeProbFcn(self, data, value):  # hour-dependent,prob to go/stay home
    hour = data[HOUR]
    if (hour == 12):
        return 0.50
    else:
        return random.random() < 1 - ((math.fabs(hour - 12) * 2) / 24.0)

def childHomeProbFcn(self, data, value):
    hour = data[HOUR]
    th = 0
    if (7 <= hour <= 9):
        th = 0.5
    elif (10 <= hour <= 14):
        th = 0
    elif (15 <= hour <= 17):
        th = 0.5
    else:  # coprifuoco
        th = 1
    return random.random() < th