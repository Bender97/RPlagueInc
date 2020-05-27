import pygame
import sys
import random
from Walker import Walker

import math

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

BLACK = (0, 0, 0)

SUSCEPTIBLE = 0
INFECTED = 1
ASYMPTOMATIC = 2
RECOVERED = 3
DEAD = 4

color = [
    (255, 255, 255), # WHITE
    (255, 50, 50), # RED
    (255, 255, 0), # YELLOW
    (50, 255, 50) # GREEN
    ]
    # no color for the dead (not drawn anymore)

CIRCLE_RADIUS = 5
INF_RADIUS = 30

INF_PROB = 0.5

NO_PEOPLE = 20
NO_INITIAL_INFECTED = 2

no_infected = NO_INITIAL_INFECTED

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('City')
fps = pygame.time.Clock()
paused = False

# person setup [x, y] = [col, row]
people = []
time = 0

def generateWalkers():
    for i in range(NO_PEOPLE):
        people.append(Walker(WIDTH, HEIGHT))

def generateInfected():
    if (NO_INITIAL_INFECTED > NO_PEOPLE):
        print("troppi infettati, sono più delle persone disponibili!")
        exit()
    infected = random.sample(people, NO_INITIAL_INFECTED)
    for person in infected:
        person.status = INFECTED
        person.TTD = 0

    people.sort(key = lambda x: x.status, reverse=True)

def getSick():

    global no_infected
    global people

    new_infected = 0

    for i in range(no_infected, NO_PEOPLE):
        if people[i].TTD>0:
            people[i].TTD -= 1
        elif people[i].TTD == 0:
            people[i].status =  INFECTED # generare asintomatici!!
            new_infected += 1

    if new_infected>0:
        no_infected += new_infected
        people.sort(key = lambda x: x.status, reverse=True)

def distance(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def spreadInfection():
       
    for i in range(no_infected, NO_PEOPLE):
        # se non sei infetto, per ogni infetto controlla se sei nella sua zona di infezione
        for j in range(no_infected):
            if (distance(people[i], people[j]) < INF_RADIUS):
                # se sei dentro, lancia il dado
                if (random.random()>INF_PROB):
                    people[i].TTD = random.randint(5, 14) # Time To Disease
                    

    
    

def update():
    # prima aggiorniamo le posizioni delle persone
    # poi permettiamo il contagio
    for person in people:
        person.update(WIDTH, HEIGHT)

    getSick()

    spreadInfection()

    for i in range(len(people)):
        print("[" + str(i) + "]: " + str(people[i].TTD))

def render():
    screen.fill(BLACK)

    font = pygame.font.Font(None, 36)
    
    for person in people:
        pygame.draw.circle(screen, color[person.status], (person.x, person.y), CIRCLE_RADIUS, 0)
        pygame.draw.circle(screen, color[person.status], (person.x, person.y), INF_RADIUS, 1)

        if (person.TTD>0):
            t = font.render(str(person.TTD), 1, (50, 255, 50))
            tp = t.get_rect(centerx = person.x, centery = person.y)
            screen.blit(t, tp)
    
    
    text = font.render("time " + str(time) + " infected: " + str(no_infected), 1, (255, 255, 255))
    textpos = text.get_rect(centerx = WIDTH/2)
    screen.blit(text, textpos)
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
        time+=1