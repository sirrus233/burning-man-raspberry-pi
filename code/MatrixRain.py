import math
import random
from Spark import Spark
from ColorCycler import ColorCycler


##
## MatrixRain
## Matrix-like spark.
##
class MatrixRain(Spark):
    def __init__(self, strip):
        self.activateChance = 0.95
        
        Spark.__init__(self, strip)


    def activate(self):
        self.active = True
        
        self.x = int(random.random() * 16)
        self.y = 0.0
        self.direction = .5 * math.pi
        self.speed = (5.0 + 10.0 * random.random()) / self.strip.frameRate
        self.bounces = False

        green = (1 << random.randint(0, 8)) - 1
        self.colorCycler = ColorCycler(0 / self.strip.frameRate, [
            (0.0, green, 0.0),
            (0.0, green, 0.0), ])
        self.radius = 0.0
        return