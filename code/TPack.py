import time
import math
from TStrip import TStrip
from ColorCycler import ColorCycler
from Spark import Spark
from MatrixRain import MatrixRain
from AcidRain import AcidRain
from Slasher import Slasher
from Bouncer import Bouncer
from Fireball import Fireball



##
## TPack
## Runs the 16x16 matrix on the pack.
## Animation 1: Matrix
## Animation 2: Acid rain
## Animation 3: Slasher
## Animation 4: Bouncer
## Animation 5: Fireball
## Animation 6: Fire and water
##
class TPack(object):
  
    # init      
    def __init__(self, dimmer, animation, cycleTime):
        # Init the strip as a matrix
        self.strip = TStrip(256, dimmer)
        self.strip.setMatrixWinding(16, 16)
        self.cycleTime = cycleTime

        self.setAnimation(animation)
        return


    def setAnimation(self, animation):
        self.animation = animation
        self.startTime = time.time()
        if self.animation == 1:
            self.init1()
        elif self.animation == 2:
            self.init2()
        elif self.animation == 3:
            self.init3()
        elif self.animation == 4:
            self.init4()
        elif self.animation == 5:
            self.init5()
        elif self.animation == 6:
            self.init6()
        return

    def init1(self):
        self.sparks = []
        for i in range(16):
            self.sparks.append(MatrixRain(self.strip))
        self.fadeRate = .80
        return


    def init2(self):
        self.sparks = []
        for i in range(30):
            self.sparks.append(AcidRain(self.strip))
        self.fadeRate = .80
        return


    def init3(self):
        self.sparks = []
        for i in range(2):
            self.sparks.append(Slasher(self.strip))
        self.fadeRate = .80
        return


    def init4(self):
        self.sparks = []
        for i in range(1):
            self.sparks.append(Bouncer(self.strip))
        self.fadeRate = .80
        return


    def init5(self):
        self.sparks = []
        for i in range(1):
            colorCycler = ColorCycler(5.0 / self.strip.frameRate, [
            (255.0, 0.0, 0.0),
            (255.0, 128.0, 0.0),
            (255.0, 255.0, 0.0),
            (255.0, 128.0, 0.0),
            ])
            self.sparks.append(Fireball(self.strip, 4.0 * math.pi, 6.0, 2.0, colorCycler))
        self.fadeRate = .80
        return


    def init6(self):
        self.sparks = []

        colorCycler = ColorCycler(5.0 / self.strip.frameRate, [
            (0.0, 0.0, 255.0),
            (0.0, 255.0, 255.0),
            ])
        self.sparks.append(Fireball(self.strip, -3.0 * math.pi, 3.5, 1.5, colorCycler))

        colorCycler = ColorCycler(5.0 / self.strip.frameRate, [
            (255.0, 0.0, 0.0),
            (255.0, 128.0, 0.0),
            (255.0, 255.0, 0.0),
            (255.0, 128.0, 0.0),
            ])
        self.sparks.append(Fireball(self.strip, 4.0 * math.pi, 7.0, 1.5, colorCycler))

        self.fadeRate = .80
        return


    # run
    # Infinite loop that runs the animation
    def run(self):
        while True:
            elapsedTime = time.time() - self.startTime
            if elapsedTime >= self.cycleTime:
                self.animation += 1
                if self.animation > 6:
                    self.animation = 1
                self.setAnimation(self.animation)

                
            self.strip.startFrame()

            self.strip.fade(self.fadeRate)

            for spark in self.sparks:
                spark.run()

            self.strip.endFrame()


    # run3
    # Runs the spark playground
    def run3(self):
        return