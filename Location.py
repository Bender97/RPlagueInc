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

class Location:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('City')
        self.fps = pygame.time.Clock()
        self.paused = False

        # person setup [x, y] = [col, row]
        self.people = []
        self.time = 0

        self.CIRCLE_RADIUS = 5
        self.INF_RADIUS = 30

        self.INF_PROB = 0.5

        self.NO_PEOPLE = 20
        self.NO_INITIAL_INFECTED = 2

        self.no_infected = self.NO_INITIAL_INFECTED

    def generateWalkers(self):
        for i in range(self.NO_PEOPLE):
            self.people.append(Walker(WIDTH, HEIGHT))

    def generateInfected(self):
        if (self.NO_INITIAL_INFECTED > self.NO_PEOPLE):
            print("troppi infettati, sono più delle persone disponibili!")
            exit()

        infected = random.sample(self.people, self.NO_INITIAL_INFECTED)
        for person in infected:
            person.status = INFECTED
            person.TTD = 0

        self.people.sort(key = lambda x: x.status, reverse=True)

    def getSick(self):

        new_infected = 0

        for i in range(self.no_infected, self.NO_PEOPLE):
            if self.people[i].TTD>0:
                self.people[i].TTD -= 1
            elif self.people[i].TTD == 0:
                self.people[i].status =  INFECTED # generare asintomatici!!
                new_infected += 1

        if new_infected>0:
            self.no_infected += new_infected
            self.people.sort(key = lambda x: x.status, reverse=True)

    def distance(self, p1, p2):
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    def spreadInfection(self):
           
        for i in range(self.no_infected, self.NO_PEOPLE):
            # se non sei infetto, per ogni infetto controlla se sei nella sua zona di infezione
            if (self.people[i].TTD<0):
                for j in range(self.no_infected):
                    if (self.distance(self.people[i], self.people[j]) < self.INF_RADIUS):
                        # se sei dentro, lancia il dado
                        if (random.random()>self.INF_PROB):
                            self.people[i].TTD = random.randint(5, 14) # Time To Disease

    def update(self):
        # prima aggiorniamo le posizioni delle persone
        # poi permettiamo il contagio
        for person in self.people:
            person.update(WIDTH, HEIGHT)

        self.getSick()

        self.spreadInfection()

    def render(self):
        self.screen.fill(BLACK)

        font = pygame.font.Font(None, 36)
        
        for person in self.people:
            pygame.draw.circle(self.screen, color[person.status], (person.x, person.y), self.CIRCLE_RADIUS, 0)
            pygame.draw.circle(self.screen, color[person.status], (person.x, person.y), self.INF_RADIUS, 1)

            if (person.TTD>0):
                t = font.render(str(person.TTD), 1, (50, 255, 50))
                tp = t.get_rect(centerx = person.x, centery = person.y)
                self.screen.blit(t, tp)
        
        
        text = font.render("time " + str(self.time) + " infected: " + str(self.no_infected), 1, (255, 255, 255))
        textpos = text.get_rect(centerx = WIDTH/2)
        self.screen.blit(text, textpos)
        pygame.display.update()
        self.fps.tick(30)

    def updateLocation(self):

        self.generateWalkers()

        self.generateInfected()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
            if not self.paused:
                self.update()
                self.render()
                self.time+=1

location = Location(WIDTH, HEIGHT)

location.updateLocation()