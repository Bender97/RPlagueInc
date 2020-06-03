SUSCEPTIBLE = 0
INCUBATION = 1
INFECTED = 2
ASYMPTOMATIC = 3
RECOVERED_FROM_ASYMPTOMATIC = 4
RECOVERED_FROM_INFECTED = 5
DEAD = 6

statusNum = 7

old_age = 65
young_age = 20

goodHealth_level = 0.8
badHealth_level = 0.5

INCUBATION_DURATION_RANGE = (2, 14)
DISEASE_DURATION_RANGE = (2, 28)
ASYMPTOMATIC_DURATION_RANGE = (7, 28)

colors = (
	( 255, 255, 255 ),	# susceptible
	( 50, 50, 255),		# incubation
	( 255, 50, 50),		# INFECTED
	( 255, 255, 50),	# asymptomatic
	( 50, 255, 50),		# recovered_from_asymptomatic
	( 50, 255, 50),		# recovered_from_infected
	)