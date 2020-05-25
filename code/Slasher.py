import math
import random
from Spark import Spark
from ColorCycler import ColorCycler


##
## Slasher
## Single fast slashes
##
class Slasher(Spark):
    def __init__(self, strip):
        self.activateChance = 10.0
        
        Spark.__init__(self, strip)


    def activate(self):
        self.active = True

        self.y = 0.0
        if random.random() < 0.5:
            self.x = -4.0 + random.random() * 16
            self.direction = .25 * math.pi
        else:
            self.x = 4 + random.random() * 16
            self.direction = .75 * math.pi

        
        self.speed = 80.0 / self.strip.frameRate
        self.bounces = False

        red = (1 << random.randint(4, 8)) - 1
        green = red * (.25 + .5 * random.random())

        self.colorCycler = ColorCycler(0 / self.strip.frameRate, [
            (red, green, 0.0),
            (red, green, 0.0), ])
        self.radius = 0.75 + 0.25 * random.random()
        return