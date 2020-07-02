import parameters as param
import structures.locations as l

"""
CHOICES
0   No Operation
1   Mandatory Mask
2   Mandatory Safe Distance
3   Quarantine for Infected Walkers
4   Close Schools
5   Close Leasures
6   Close Workplaces
"""

N_CHOICES = 7

# Choices
CH_NOOP = 0
CH_MAND_MASKS = 1
CH_MAND_DIST = 2
CH_QUAR_INF = 3
CH_CL_SCHOOLS = 4
CH_CL_LEISURES = 5
CH_CL_WORK = 6

CH_STR = {
    CH_MAND_MASKS: "mandatory masks",
    CH_MAND_DIST: "mandatory safe distance",
    CH_QUAR_INF: "quarantined infected",
    CH_CL_SCHOOLS: "school closed",
    CH_CL_LEISURES: "leisure places closed",
    CH_CL_WORK: "work places closed"
}

# Action types
ENACT = 0
ABOLISH = 1

ACT_STR = {
    ENACT: "enacted",
    ABOLISH: "abolished"
    }

# Effects
P_INF_MULT = 0
ADD_DISCONTENT_NOW = 1
ADD_DISCONTENT_CONST = 1
CLOSE_LOCS = 3
OPEN_LOCS = 4
SET_SAFE_DIST = 5
QUAR_WALKERS = 6
FREE_WALKERS = 7

# Effects of actions dictionary

EFFECTS_DICT = {
    CH_MAND_MASKS: {
        ENACT   : {P_INF_MULT: 0.5 , ADD_DISCONTENT_CONST:  50, ADD_DISCONTENT_NOW: 200},
        ABOLISH : {P_INF_MULT: 2   , ADD_DISCONTENT_CONST: -50}
    },
    CH_MAND_DIST: {
        ENACT   : {SET_SAFE_DIST: 1, ADD_DISCONTENT_CONST:  50, ADD_DISCONTENT_NOW: 200},
        ABOLISH : {SET_SAFE_DIST: 0, ADD_DISCONTENT_CONST: -50}
    },
    CH_QUAR_INF: {
        ENACT   : {QUAR_WALKERS: param.INFECTED, ADD_DISCONTENT_NOW: 200},
        ABOLISH : {FREE_WALKERS: param.INFECTED}
    },
    CH_CL_SCHOOLS: {
        ENACT   : {CLOSE_LOCS: l.SCHOOL, ADD_DISCONTENT_NOW: 200},
        ABOLISH : {OPEN_LOCS: l.SCHOOL}
    },
    CH_CL_LEISURES: {
        ENACT   : {CLOSE_LOCS: l.LEISURE, ADD_DISCONTENT_NOW: 600},
        ABOLISH : {OPEN_LOCS: l.LEISURE}
    },
    CH_CL_WORK: {
        ENACT   : {CLOSE_LOCS: l.WORKPLACE, ADD_DISCONTENT_NOW: 400},
        ABOLISH : {OPEN_LOCS: l.WORKPLACE}
    }
}

def getMaxChoicesDiscontent ():
    discontent = 0
    for ch in EFFECTS_DICT.values():
        effs = ch[ENACT]
        for eff in effs.keys():
            if eff == ADD_DISCONTENT_CONST or eff == ADD_DISCONTENT_NOW:
                discontent += effs[eff]
        # end for
    # end for
    return discontent

def getChoicesMask (engine):
    # 0 -> noop, 1-6 -> ENACT, 7-12 -> ABOLISH
    # set noop to allowed
    choices_mask = [True]

    effects = list(engine.in_effect.values())
    durations = list(engine.meas_durations.values())

    for i in range(len(effects)):
        # allowed if it is not in effect and the duration reached 0
        allowed = not effects[i] and durations[i] == 0
        choices_mask.append(allowed)

    for i in range(len(effects)):
        # allowed if it is in effect and the duration reached 0
        allowed = effects[i] and durations[i] == 0
        choices_mask.append(allowed)

    return choices_mask



def setupChoices (engine):
    ch_effects = {}
    durations = {}

    for e in EFFECTS_DICT.keys():
        ch_effects[e] = False
        durations[e] = 0

    # choices dependent variables
    engine.daily_discontent = 0
    engine.closed_locs = []
    engine.quarantine = []
    engine.safe_dist = 0
    engine.virus.masks_malus = 1.

    engine.in_effect = ch_effects
    engine.meas_durations = durations
# end setupChoices

def isEnacted (choice, engine):
    return engine.in_effect[choice]
# end inEnacted

def makeChoice (type, choice, engine):

    # for each measure reduce by 1 day of duration
    for k in engine.meas_durations.keys():
        if engine.meas_durations[k] > 0:
            engine.meas_durations[k] -= 1

    # if the choice is noop don't do anything
    if choice == CH_NOOP:
        return False

    # if the choice to enact is already in effect or the choice to abolish is not in effect then exit (NO OP)
    if (type == ENACT and engine.in_effect[choice]) or (type == ABOLISH and not engine.in_effect[choice]):
        return False

    # get effects on choice
    effects = EFFECTS_DICT[choice][type]

    # apply all effects of the choice
    for e in effects.keys():
        applyEffect(e, effects[e], engine)

    #print("Choice " + CH_STR[choice] + " was " + ACT_STR[type])
    engine.choice_str = [CH_STR[choice] + '\n' + ACT_STR[type], type == ENACT]

    # publish enact/abolish on the engine choices
    effect_result = type == ENACT
    engine.in_effect[choice] = effect_result
    engine.meas_durations[choice] = param.MEASURE_DURATION

    return True

# end makeChoice

def applyEffect (effect, value, engine):

    if effect == P_INF_MULT:
        engine.virus.masks_malus *= value

    elif effect == ADD_DISCONTENT_NOW:
        engine.discontent += value

    elif effect == ADD_DISCONTENT_CONST:
        engine.daily_discontent += value

    elif effect == CLOSE_LOCS:
        engine.closed_locs.append(value)

    elif effect == OPEN_LOCS:
        engine.closed_locs.remove(value)

    elif effect == SET_SAFE_DIST:
        engine.safe_dist = value

    elif effect == QUAR_WALKERS:
        engine.quarantine.append(value)

    elif effect == FREE_WALKERS:
        engine.quarantine.remove(value)

# end applyEffect