
import pygame
import engine.statistics as stats
import time
import matplotlib.pyplot as plt
import structures.locations as ls
import walkers.healthState as h

def initRender(engine):

    border = 20
    padding = 20

    engine.maxWidth = 500         # static
    engine.maxHeight = border     # dinamically updated

    # these two indicates the next position of a location
    currentdx = border
    currentdy = border

    for locs in engine.locs:
        for loc in locs:

            #1) check the current location can fit the window (accounting also the border value)

            if (currentdx + loc.size_x + border < engine.maxWidth):

                engine.locPos[loc.type].append(pygame.Rect(currentdx, currentdy, loc.size_x, loc.size_y))
                # prepare for next 
                currentdx += loc.size_x + padding

                # check for maxHeight (for next line height)
                tempy = currentdy + loc.size_y
                if (tempy > engine.maxHeight):
                    engine.maxHeight = tempy

            else:
                # go to next line
                currentdy = engine.maxHeight + padding
                currentdx = border
                engine.locPos[loc.type].append(pygame.Rect(currentdx, currentdy, loc.size_x, loc.size_y))

                currentdx += loc.size_x + padding

    engine.maxHeight += border

    pygame.init()

    engine.myfont = pygame.font.SysFont("monospace", 15)

    engine.screen = pygame.display.set_mode((engine.maxWidth, engine.maxHeight))

    pygame.display.set_caption('City')
    engine.fps = pygame.time.Clock()
    engine.paused = False

def renderize(engine, pause = 0.5):
    statistics = list(stats.computeStatistics(engine).items())

    engine.xdata.append(engine.day_counter)

    engine.ydata[0].append(statistics[0][1])
    engine.ydata[1].append(statistics[1][1])
    engine.ydata[2].append(statistics[2][1])
    engine.ydata[3].append(statistics[3][1])

    plt.plot(engine.xdata, engine.ydata[0], 'bo-')
    plt.plot(engine.xdata, engine.ydata[1], 'ro-')
    plt.plot(engine.xdata, engine.ydata[2], 'go-')
    plt.plot(engine.xdata, engine.ydata[3], 'ko-')

    engine.day_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                engine.paused = not engine.paused
    
    if not engine.paused:
        engine.screen.fill((0, 0, 0))

        for locs in engine.locs:
            idx = 0
            for loc in locs:

                posx = engine.locPos[loc.type][idx][0]
                posy = engine.locPos[loc.type][idx][1]

                pygame.draw.rect(engine.screen, ls.colors[loc.type], engine.locPos[loc.type][idx])
                label = engine.myfont.render(ls.labels[loc.type], 1, (255, 255, 255))
                engine.screen.blit(label, (posx, posy-17))
                
                for walkerType in range(h.statusNum):
                    for walker in loc.walkers[walkerType]:
                        pygame.draw.circle(engine.screen, h.colors[walkerType], (posx+walker.x, posy+walker.y), 3, 0)
                idx += 1

    pygame.display.update()
    engine.fps.tick(30)
    
    plt.legend(loc = 'upper left', labels = ('susceptibles + asymptomatics + incubation', 'infected (disease)', 'recovered', 'dead'))
    plt.pause(pause)