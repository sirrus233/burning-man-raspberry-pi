import math
import random
from ColorCycler import ColorCycler


##
## Spark
## A shiny object that races around the screen.
##
class Spark(object):
    # init
    def __init__(self, strip):
        self.strip = strip
        self.active = False
        return


    def run(self):
        if not self.active:
            self.maybeActivate()
            return
				
        self.colorCycler.cycle()

        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed

        self.x += dx
        self.y += dy

        if (self.x < 0 and dx < 0) or (self.x > 16 + self.radius and dx > 0) or (self.y < 0 and dy < 0) or (self.y > 15 + self.radius and dy > 0):
            if self.bounces:
                self.bounce()
            else:
                self.active = False

        if self.radius == 0.0:
            x = int(self.x)
            y = int(self.y)
            if x >= 0 and x <16 and y >= 0 and y < 16:
                self.strip.augmentGridPixel(x, y, self.colorCycler.currentColor)
        else:
            self.strip.drawBall(self.x, self.y, self.radius, self.colorCycler.currentColor)
        return


    def maybeActivate(self):
        if random.random() < self.activateChance / self.strip.frameRate:
            self.activate()
        return


    def activate(self):
        self.active = True
        
        self.x = random.random() * 16
        self.y = random.random() * 16
        self.colorCycler = ColorCycler(1 / self.strip.frameRate, [(255.0, 0.0, 0.0), (0.0, 0.0, 255.0)])
        self.radius = 2.0

        self.direction = random.random() * 2 * math.pi
        self.speed = 5.0 / self.strip.frameRate
        return


    def bounce(self):
        if self.x < 0:
            self.x = - self.x
            self.direction = math.pi - self.direction
        if self.y < 0:
            self.y = - self.y
            self.direction = 2.0 * math.pi - self.direction
        if self.x >= 16:
            self.x = 16.0
            self.direction = math.pi - self.direction
        if self.y >= 16.0:
            self.y = 16.0
            self.direction = 2.0 * math.pi - self.direction
        self.direction = self.direction + math.pi * (-0.1 + 0.2 * random.random())
        while self.direction < 0:
            self.direction += 2.0 * math.pi
        while self.direction >= 2.0 * math.pi:
            self.direction -= 2.0 * math.pi
        return