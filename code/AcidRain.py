import math
import random
from Spark import Spark
from ColorCycler import ColorCycler


##
## AcidRain
## Slashing acid rain
##
class AcidRain(Spark):
    def __init__(self, strip):
        self.activateChance = 0.95
        
        Spark.__init__(self, strip)


    def activate(self):
        self.active = True
        
        self.x = int(random.random() * 32)
        self.y = 0.0
        self.direction = .75 * math.pi
        self.speed = (10.0 + 20.0 * random.random()) / self.strip.frameRate
        self.bounces = False

        value = (1 << random.randint(4, 8)) - 1
        self.colorCycler = ColorCycler(0 / self.strip.frameRate, [
            (value, 0.0, value),
            (value, 0.0, value), ])
        self.radius = 0.0
        return