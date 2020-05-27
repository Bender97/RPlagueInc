import random

import structures.healthState as h


class Walker:

	def __init__(self, width, height,age,disobedience):
		self.status = h.SUSCEPTIBLE
		self.x = random.randint(0,width)
		self.y = random.randint(0,height)
		self.healthLevel = random.uniform(0.7, 1)
		self.healingLevel = 0 #tasso di guarigione DAL VIRUS
		self.age= age
		self.disobedience = disobedience


	def move(self, x, y):
		self.x = x
		self.y = y

	def setStatus(self, status):
		self.status = status

	def isInfected(self):
		return self.status==h.INFECTED

	def isSubsceptible(self):
		return self.status == h.SUSCEPTIBLE