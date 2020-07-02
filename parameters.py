
#########################################
# NET PARAMS
#########################################

NET_GAMMA = 0.95
LEARNING_RATE = 0.001

EPOCHS = 20

MEMORY_SIZE = 20000
BATCH_SIZE = 32
STATUS_WINDOW = 6

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995

YAML_PATH 	= "model.yaml"
MODEL_PATH 	= "model.h5"

#########################################
#########################################




#########################################
# SIMULATION PARAMETERS
#########################################

ENV_NAME = "engine-v0"

INITIAL_CASES 	= 5
N_HOUSES 		= 100

VIRUS_RANGE 		= 2
VIRUS_P_INFECTION 	= 0.3
VIRUS_SEVERITY 		= 0.8
VIRUS_LETHALITY 	= 0.4

INCUBATION_DURATION_RANGE = (2, 14)
DISEASE_DURATION_RANGE = (2, 28)
ASYMPTOMATIC_DURATION_RANGE = (7, 28)

# discontent values
FOOD_DAILY_DISCONTENT		= 100	# df
LEISURE_DAILY_DISCONTENT	= 10	# dl

MAX_MONEY_PER_HOUSE = 10000

# infection delta curve param
RELU_PARAM = 0.2

# reward weights
ALPHA = 10 # h(n) susc. + recov.
BETA = -200 # delta i(n) infected gradient
GAMMA = 600 # M(n) mean wealth
DELTA = -30 # D(n) discontent
EPSILON = -100 # d(n) deads
ZETA = -2 # choice taken in turn n

#########################################
#########################################


#########################################
# HEALTHSTATE STATUS PARAMETERS
#########################################

goodHealth_level = 0.8
badHealth_level = 0.5

old_age = 65
young_age = 20

SUSCEPTIBLE = 0
INCUBATION = 1
INFECTED = 2
ASYMPTOMATIC = 3
RECOVERED_FROM_ASYMPTOMATIC = 4
RECOVERED_FROM_INFECTED = 5
DEAD = 6

statusNum = 7

#########################################
#########################################


#########################################
# RENDERING PARAMETERS
#########################################

WHITE = ( 255, 255, 255 )

colors = (
	WHITE,				# susceptible
	( 50, 50, 255),		# incubation
	( 255, 50, 50),		# INFECTED
	( 255, 255, 50),	# asymptomatic
	( 50, 255, 50),		# recovered_from_asymptomatic
	( 50, 255, 50),		# recovered_from_infected
	)

FONTSIZE = 15

PADDING = 20
BORDER = 20

MONEYOFFSET = 17

FPS = 30

#########################################
#########################################