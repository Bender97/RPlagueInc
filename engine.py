import pygame
import sys
import random
from Walker import Walker

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

BLACK = (0, 0, 0)

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

CIRCLE_RADIUS = 5
INF_RADIUS = 30

NO_PEOPLE = 10
NO_INITIAL_INFECTED = 2

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('City')
fps = pygame.time.Clock()
paused = False

# Ball setup [x, y] = [col, row]
people = []

def generateWalkers():
	for i in range(NO_PEOPLE):
		people.append(Walker(WIDTH, HEIGHT))

def generateInfected():
	if (NO_INITIAL_INFECTED > NO_PEOPLE):
		print("troppi infettati, sono pi delle persone disponibili!")
		exit()
	infected = random.sample(people, NO_INITIAL_INFECTED)
	for person in infected:
		person.status = INFECTED

def update():
	for person in people:
		person.update(WIDTH, HEIGHT)

def render():
    screen.fill(BLACK)
    for person in people:
    	pygame.draw.circle(screen, color[person.status], (person.x, person.y), CIRCLE_RADIUS, 0)
    	pygame.draw.circle(screen, color[person.status], (person.x, person.y), INF_RADIUS, 1)
    pygame.display.update()
    fps.tick(30)


generateWalkers()

generateInfected()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if not paused:
        update()
        render()