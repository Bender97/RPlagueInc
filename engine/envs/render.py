import pygame
import engine.statistics as stats
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import structures.locations as ls
import parameters as param
import os

colors = ['b,-', 'r,-', 'g,-', 'k,-', 'c,-', 'm,-']

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

def initPlt(engine, figure, xlabel, ylabel, n_subplots):
    
    plt.figure(figure).show()
    plt.clf()
    engine.figs[figure] = []

    for i in range(n_subplots):
        engine.figs[figure].append(plt.plot([], [], colors[i])[0])

    plt.axhline(y=0, color='grey', linestyle='--')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def renderFramePlt(engine, figure, new_xdata, new_ydata, labels):
    
    fig = plt.figure(figure)

    for i in range(len(new_ydata)):
        line = engine.figs[figure][i]
        line.set_xdata(np.append(line.get_xdata(), new_xdata))
        line.set_ydata(np.append(line.get_ydata(), new_ydata[i]))
        line.axes.relim()
        line.axes.autoscale_view()


    plt.legend(loc = 'upper left', labels = labels)

    if engine.choice_str != None:

        vline_color = 'red' if engine.choice_str[1] else 'blue'

        _, _, ymin, ymax = plt.axis()

        text_pos = random.uniform(ymin, ymax)

        plt.axvline(x=new_xdata, color=vline_color, linewidth=0.5)
        plt.text(x=new_xdata, y=text_pos, s=engine.choice_str[0], color=vline_color, fontsize='xx-small')


    fig.canvas.draw()
    fig.canvas.flush_events()


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