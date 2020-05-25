from TStrip import TStrip
import time



##
## TBike
## Runs the bike lights
class TBike(object):

    # init
    def __init__(self, dimmer):
        # Init the strip and set up our geometry
        self.strip = TStrip(87, dimmer)
        self.iHeadLight = 36
        self.iTailLight1 = 75
        self.iTailLight2 = 76
        self.sides = [
            (34, 38),
            (33, 39),
            (32, 40),
            (31, 41),
            (30, 42),
            (29, 43),
            (28, 44),
            (27, 45),
            (26, 46),
            (25, 47),
            (24, 48),
            (23, 49),
            (22, 50),
            (21, 51),
            (20, 52),
            (19, 53),
            (18, 54),
            (17, 55),
            (16, 56),
            (15, 57),
            (14, 58),
            (13, 59),
            (12, 60),
            (11, 61),
            (10, 62),
            ( 9, 63),
            ( 8, 64),
            ( 7, 65),
            ( 6, 66), 
            ( 5, 67), 
            ( 4, 68), 
            ( 3, 69),
            ( 2, 70),
            ( 1, 71),
            ( 0, 72) ]
        self.sideLevels = [0.0 for i in range(len(self.sides))]

        # Configure ourselves
        self.headLightColor = (0xff, 0xff, 0xff)
        self.tailLightColor = (0xff, 0x00, 0x00)
        self.sparkColor = (0xff, 0xff, 0xff)
        self.glowColor = (0xff, 0x00, 0xff)
        self.sparkSpeed = 30
        self.fadeSpeed = 12.0
        self.persistence = 1.0 - (self.fadeSpeed / self.strip.frameRate)

        # Init ourselves
        self.strip.setPixel(self.iHeadLight, self.headLightColor)
        self.strip.setPixel(self.iTailLight1, self.tailLightColor)
        self.strip.setPixel(self.iTailLight2, self.tailLightColor)
        self.sparkPos = 0

        return


    def setSide(self, iPixel, color):
        self.strip.setPixel(self.sides[iPixel][0], color)
        self.strip.setPixel(self.sides[iPixel][1], color)
        return


    def run(self):
        while True:
            self.strip.startFrame()
            
            # Move the spark
            self.sparkPos += self.sparkSpeed / self.strip.frameRate
            if self.sparkPos >= len(self.sides):
                self.sparkPos = 0
            pos = int(self.sparkPos)

            # Fade every pixel
            for iPixel in range(len(self.sides)):
                self.sideLevels[iPixel] = self.sideLevels[iPixel] * self.persistence

            # Set the spark pixel to maximum
            self.sideLevels[pos] = 1.0

            # Apply the pixel levels
            for iPixel in range(len(self.sides)):
                red = int(self.sideLevels[iPixel] * self.glowColor[0])
                green = int(self.sideLevels[iPixel] * self.glowColor[1])
                blue = int(self.sideLevels[iPixel] * self.glowColor[2])
                self.setSide(iPixel, (red, green,blue))

            # Draw the spark
            self.setSide(pos, self.sparkColor)

            self.strip.endFrame()