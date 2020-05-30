from structures.locations import *
import random

from engine.virus import Virus
from walkers.Walker import Walker

import walkers.healthState as h

import time

import matplotlib.pyplot as plt

class DynamicUpdate():
    #Suppose we know the x range

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'ro-')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        #Other stuff
        self.ax.grid()
        ...

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)

loc = buildDefaultLocation(HOME)
loc.initRendering()

for i in range(20):
                    
    walker = Walker( 640, # loc_width
                     480, # loc_height
                     random.randint(1, 100), # age
                     1,   # disobedience
                     loc, # where it lives
                     None)
    
    if (random.random()<0.2):
        walker.setStatus(h.INCUBATION)
        walker.updateVirusTimer(value = random.randint(h.INCUBATION_DURATION_RANGE[0], h.INCUBATION_DURATION_RANGE[1]))

    loc.enter(walker)

day_counter = 0

d = DynamicUpdate()
plt.ion()
d.on_launch()
xdata = []
ydata = []

while(True):
    for hour in range(24):

        loc.run1HOUR(virus)

        for incubated in loc.walkers[h.INCUBATION]:
            if (incubated.getVirusTimer()>0):
                incubated.updateVirusTimer()
        
        for asymptomatic in loc.walkers[h.ASYMPTOMATIC]:
            if (asymptomatic.getVirusTimer()>0):
                asymptomatic.updateVirusTimer()

        for infected in loc.walkers[h.INFECTED]:
            if (infected.getVirusTimer()>0):
                infected.updateVirusTimer()
            else:
                flag = virus.tryDeath(infected)

                loc.walkers[h.INFECTED].remove(infected)

                if (flag):
                    loc.walkers[h.DEAD].append(infected)
                    print("+1 DEAD")
                else:
                    loc.walkers[h.RECOVERED].append(infected)
        
        xdata.append(day_counter*24 + hour)
        ydata.append(len(loc.walkers[h.SUSCEPTIBLE]))

        d.on_running(xdata, ydata)

        loc.render(virus)
        time.sleep(0.5)

    day_counter += 1