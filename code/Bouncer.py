import math
import random
from Spark import Spark
from ColorCycler import ColorCycler


##
## Bouncer
## Bounces around the screen
##
class Bouncer(Spark):
    def __init__(self, strip):
        self.activateChance = 60.0
        
        Spark.__init__(self, strip)


    def activate(self):
        self.active = True

        self.x = 16.0 * random.random()
        self.y = 16.0 * random.random()
        self.direction = 2 * math.pi * random.random()
        self.speed = 60.0 / self.strip.frameRate
        self.radius = 2.0
        self.bounces = True

        if random.random() < 1.0:
            self.colorCycler = ColorCycler(5.0 / self.strip.frameRate, [
                (0.0, 0.0, 255.0),
                (0.0, 128.0, 128.0),
                (0.0, 255.0, 0.0),
                (0.0, 128.0, 128.0),
                ])
        else:
            self.colorCycler = ColorCycler(5.0 / self.strip.frameRate, [
                (255.0, 0.0, 0.0),
                (255.0, 128.0, 0.0),
                (255.0, 255.0, 0.0),
                (255.0, 128.0, 0.0),
                ])
        return
