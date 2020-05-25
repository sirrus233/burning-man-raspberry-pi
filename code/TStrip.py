import spidev
import time


##
## TStrip
## This is the base class that talks to a DotStar chain.
## We are 
##
class TStrip(object):

    # init
    def __init__(self, cPixels, dimmer):
        self.frameRate = 60     #Target frame rate in Hz
        self.dimmer = dimmer    # Dim every pixel by this many bits
        
        # We use spidev to talk serial to the DotStar
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz=8000000

        # Create the pixel array
        self.pixels = [(0.0, 0.0, 0.0) for i in range(0, cPixels)]

        # Pin the entire system to 25 full-brightness LEDs or equivalent
        # This prevents us from overloading the power supply.
        self.maxTotalBrightness = 25 * 3 * 0xff

        return


    # setMatrixWinding
    # This is only half finished. Right now it only works for the Adafruit 16x16 matrix.
    # Creates a mapping array for writing to a matrix-style DotStar
    def setMatrixWinding(self, width, height):
        # mapPixels will map from (x,y) to a pixel index
        self.mapPixels = [[0 for j in range(height)] for i in range(width)]

        # We're gonna walk the whole grid in a winding pattern
        x = 0
        y = 0
        yDir = 1
        iPixel = 0
        while True:
            self.mapPixels[x][y] = iPixel
            iPixel += 1
            y += yDir
            if y < 0:
                x += 1
                y = 0
                yDir = 1
            if y >= height:
                x += 1
                y = height - 1
                yDir = -1
            if x >= width:
                return


    # writeBrightness
    # Push a single brightness byte down the wire, capping it if we've reached
    # our maximum allowable brightness.
    def writeBrightness(self, brightnessIn):
        brightness = int(brightnessIn)
        brightness = brightness >> self.dimmer
        if self.cumulativeBrightness > self.maxTotalBrightness:
            brightness = 0
        self.spi.xfer2([brightness])
        self.cumulativeBrightness += brightness
        return


    # setPixel
    # Set the (r,g,b) color of a pixel
    def setPixel(self, iPixel, color):
        self.pixels[iPixel] = color
        return


    # setGridPixel
    # Set the (r,g,b) color of a matrix pixel
    def setGridPixel(self, x, y, color):
        iPixel = self.mapPixels[x][y]
        self.pixels[iPixel] = color
        return


    ## augmentGridPixel
    # If the existing pixel is dimmer than the specified color, set it to the specified color
    def augmentGridPixel(self, x, y, color):
        iPixel = self.mapPixels[x][y]

        red = self.pixels[iPixel][0]
        if color[0] > red:
            red = color[0]

        green = self.pixels[iPixel][1]
        if color[1] > green:
            green = color[1]

        blue = self.pixels[iPixel][2]
        if color[2] > blue:
            blue = color[2]

        self.pixels[iPixel] = (red, green, blue)
        return



    # paint
    # Sets the entire strip to a specified color
    def paint(self, color):
        for i in range(0, len(self.pixels)):
            self.pixels[i] = color
        return

    # fade
    # Fades the entire strip by a given amount
    def fade(self, retain):
        for iPixel in range(len(self.pixels)):
            pixel = self.pixels[iPixel]
            self.pixels[iPixel] = (pixel[0] * retain, pixel[1] * retain, pixel[2] * retain)


    # drawBall
    # Draws a ball at a specified location
    def drawBall(self, xCenter, yCenter, radius, color):
        distMax = radius * radius
        for x in range(int(xCenter - radius - 1), int(xCenter + radius + 2)):
            for y in range(int(yCenter - radius - 1), int(yCenter + radius + 2)):
                dist = (xCenter - x) * (xCenter - x) + (yCenter - y) * (yCenter - y)
                if dist <= distMax:
                    if x >= 0 and x <= 15 and y >= 0 and y <= 15:
                        ratio = 1.0 - (dist / distMax)
                        self.augmentGridPixel(x, y, (ratio * color[0], ratio * color[1], ratio * color[2]))
        return

        
    # startFrame
    # Call this at the start of each frame
    def startFrame(self):
        self.frameStartTime = time.time()
        return
    

    # endFrame
    # We're done with this frame. Push all the pixel data down the wire.
    def endFrame(self):
        self.cumulativeBrightness = 0
        
        # Header block
        self.spi.xfer2([0x00, 0x00, 0x00, 0x00])

        # LEDs
        for i in range(0, len(self.pixels)):
            self.spi.xfer2([0xff])
            self.writeBrightness(self.pixels[i][2]) # B
            self.writeBrightness(self.pixels[i][1]) # G
            self.writeBrightness(self.pixels[i][0]) # R

        # End block
        self.spi.xfer2([0xff, 0xff, 0xff, 0xff])
        for i in range(0, 1 + (len(self.pixels) >> 5)):
            self.spi.xfer2([0x00, 0x00, 0x00, 0x00])

        # Sleep until it's time for the next frame
        extraTime = (1 / self.frameRate) - (time.time() - self.frameStartTime)
        if extraTime > 0:
            time.sleep(extraTime)

        return