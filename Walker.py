import random

SUSCEPTIBLE = 0
INFECTED = 1
ASYMPTOMATIC = 2
HEALED = 3
DEAD = 4

color = [
	(255, 255, 255), # WHITE
	(255, 50, 50), # RED
	(255, 255, 0), # YELLOW
	(50, 255, 50) # GREEN
	]
	# no color for the dead (removed)

class Walker:
	def __init__(self, width, height):
		self.x = random.randint(0, width)
		self.y = random.randint(0, height)
		self.status = SUSCEPTIBLE

	def update(self, width, height):
		tempx = self.x + random.randint(-10, 10)
		tempy = self.y + random.randint(-10, 10)
		
		#col check
		if (tempx<0):
			self.x = 0
		elif tempx>width:
			self.x = width
		else:
			self.x = tempx

		#row check
		if (tempy<0):
			self.y = 0
		elif tempy>height:
			self.y = height
		else:
			self.y = tempy
