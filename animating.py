import pygame
import sys
import random

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

CIRCLE_RADIUS = 5
INF_RADIUS = 30

NO_BALLS = 10

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()
paused = False

# Ball setup [x, y] = [col, row]
ball_pos = []

def generateBalls():
	for i in range(NO_BALLS):
		ball_pos.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])

def update():
	for i in range(NO_BALLS):
		tempx = ball_pos[i][0] + random.randint(-10, 10)
		tempy = ball_pos[i][1] + random.randint(-10, 10)
		
		#col check
		if (tempx<0):
			ball_pos[i][0] = 0
		elif tempx>WIDTH:
			ball_pos[i][0] = WIDTH
		else:
			ball_pos[i][0] = tempx

		#row check
		if (tempy<0):
			ball_pos[i][1] = 0
		elif tempy>HEIGHT:
			ball_pos[i][1] = HEIGHT
		else:
			ball_pos[i][1] = tempy

def render():
    screen.fill(BLACK)
    for i in range(NO_BALLS):
    	pygame.draw.circle(screen, WHITE, ball_pos[i], CIRCLE_RADIUS, 0)
    	pygame.draw.circle(screen, RED, ball_pos[i], INF_RADIUS, 1)
    #pygame.draw.circle(screen, WHITE, ball_pos2, CIRCLE_RADIUS, 0)
    #pygame.draw.circle(screen, GREEN, ball_pos3, CIRCLE_RADIUS, 0)
    pygame.display.update()
    fps.tick(30)


generateBalls()

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