import pygame
import engine.statistics as stats
import time
import matplotlib.pyplot as plt
import structures.locations as ls
import parameters as param
import os

colors = ['bo-', 'ro-', 'go-', 'ko-', 'co-']

def initPyGame(engine, border=20, padding=20, maxWidth = 500, name_of_window='City'):

    pygame.init()
    #os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (700,50)

    engine.myfont = pygame.font.SysFont("monospace", param.FONTSIZE)


    pygame.display.set_caption(name_of_window)
    engine.fps = pygame.time.Clock()
    engine.paused = False 

    engine.maxWidth = maxWidth         # static
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

                engine.maxHeight += loc.size_y + padding

    engine.maxHeight += border

    engine.screen = pygame.display.set_mode((engine.maxWidth, engine.maxHeight))

def initPlt(engine):
    engine.day_counter = 0
    engine.xdata = []
    engine.ydata = [[], [], [], []]

    plt.figure(1)

    plt.clf()

    plt.xlabel('number of days')
    plt.ylabel('people')

def initPltState(engine):
    engine.day_counter = 0
    engine.xdata = []
    engine.ydatastate = [[], [], [], [], [], []]

    plt.figure(2)

    plt.clf()

    plt.xlabel('number of days')
    plt.ylabel('state')


def renderFramePlt(engine):
    statistics_dict = list(stats.computeStatistics(engine).values())

    to_graph = [stats.S, stats.I, stats.R, stats.D]
    statistics = [statistics_dict[k] for k in to_graph]

    engine.xdata.append(engine.day_counter)

    plt.figure(1)

    for i in range(len(to_graph)):
        engine.ydata[i].append(statistics[i])
        plt.plot(engine.xdata, engine.ydata[i], colors[i])

    engine.day_counter += 1
    plt.legend(loc = 'upper left', labels = ('susceptibles + asymptomatics + incubation: '+ str(statistics[0]),
                                             'infected (disease): '                       + str(statistics[1]),
                                             'recovered: '                                + str(statistics[2]),
                                             'dead: '                                     + str(statistics[3])))
    plt.pause(0.01)

def renderFramePyGame(engine):

    engine.screen.fill((0, 0, 0))

    for locs in engine.locs:
        idx = 0
        for loc in locs:

            posx = engine.locPos[loc.type][idx][0]
            posy = engine.locPos[loc.type][idx][1]

            pygame.draw.rect(engine.screen, ls.colors[loc.type], engine.locPos[loc.type][idx])
            label = engine.myfont.render(ls.labels[loc.type], 1, param.WHITE)
            if loc.type == ls.HOME:
                food = engine.myfont.render(str(loc.food_qty), 1, param.WHITE)
                money = engine.myfont.render(str(loc.money), 1, param.WHITE)
                engine.screen.blit(food, (posx, posy))
                engine.screen.blit(money, (posx, posy+param.MONEYOFFSET))


            engine.screen.blit(label, (posx, posy-param.MONEYOFFSET))
            
            for walkerType in range(param.statusNum):
                for walker in loc.walkers[walkerType]:
                    walker_x, walker_y = engine.walker_pool.getCoords(walker)
                    pygame.draw.circle(engine.screen, param.colors[walkerType], (posx+int(walker_x), posy+int(walker_y)), 3, 0)
            idx += 1

    pygame.display.update()
    engine.fps.tick(param.FPS)

def renderFramePltState(engine, state):

    plt.figure(2)

    for i in range(5):
        print(i)
        engine.ydatastate[i].append(state[i])
        plt.plot(engine.xdata, engine.ydatastate[i], colors[i])

    plt.legend(loc = 'upper left', labels = ('h_n: '        + str("{:.2f}".format(state[0])),
                                             'delta_i_n: '  + str("{:.2f}".format(state[1])),
                                             'M_n: '        + str("{:.2f}".format(state[2])),
                                             'D_n: '        + str("{:.2f}".format(state[3])),
                                             'd_n: '        + str("{:.2f}".format(state[4])),
                                             'reward: '     + str("{:.2f}".format(state[5]))))
    plt.pause(0.01)