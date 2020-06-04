import random
import engine.schedules.schedules as s

# some probability functions
def forSure(data, value):
    return True

def uniformChoice(data, value):
    return random.random() < value

def tryDisobey(data, value):
    return random.random() < data[s.WALKER].disobedience

def adultHomeProbFcn(data, value):  # hour-dependent,prob to go/stay home
    hour = data[HOUR]
    if (hour == 12):
        return 0.50
    else:
        return random.random() < 1 - ((math.fabs(hour - 12) * 2) / 24.0)

def childHomeProbFcn(data, value):
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