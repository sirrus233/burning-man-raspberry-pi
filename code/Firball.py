import math
import random
from Spark import Spark
from ColorCycler import ColorCycler


##
## Fireball
## Races around the screen in a flaming circle around the screen
##
class Fireball(Spark):
    def __init__(self, strip, orbitalSpeed, orbitalRadius, radius, colorCycler):
        self.activateChance = 60.0
        
        Spark.__init__(self, strip)

        self.angle = 2.0 * math.pi * random.random()
        self.angularSpeed = orbitalSpeed / self.strip.frameRate
        self.orbitalRadius = orbitalRadius
        self.xCenter = 7.5
        self.yCenter = 7.5

        self.radius = radius
        self.bounces = False

        self.colorCycler = colorCycler



    def activate(self):
        self.active = True
        return


    def run(self):
        if not self.active:
            self.maybeActivate()
            return
				
        self.colorCycler.cycle()

        self.angle = self.angle + self.angularSpeed
        if self.angle < 0.0:
            self.angle += 2.0 * math.pi
        if self.angle >= 2.0 * math.pi:
            self.angle -= 2.0 * math.pi

        self.x = self.xCenter + self.orbitalRadius * math.cos(self.angle)
        self.y = self.yCenter + self.orbitalRadius * math.sin(self.angle)

        if self.radius == 0.0:
            x = int(self.x)
            y = int(self.y)
            if x >= 0 and x <16 and y >= 0 and y < 16:
                self.strip.augmentGridPixel(x, y, self.colorCycler.currentColor)
        else:
            self.strip.drawBall(self.x, self.y, self.radius, self.colorCycler.currentColor)
        return