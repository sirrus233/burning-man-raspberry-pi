##
## ColorCycler
## Provides a simple mechanism for cycling between multiple colors
##
class ColorCycler(object):

	# init
	def __init__(self, rate, colors):
		self.rate = rate
		self.colors = colors

		self.iColor = 0.0
		self.calculateColor()
		return



	# cycle
	# Move ahead one iteration
	def cycle(self):
		self.iColor += self.rate
		while self.iColor >= len(self.colors):
			self.iColor -= len(self.colors)
		self.calculateColor()
		return


	# calculateColor
	# Figures out our current color based on our cycle
	def calculateColor(self):
		color1 = self.colors[int(self.iColor)]

		iColor2 = int(self.iColor) + 1
		if iColor2 >= len(self.colors):
			iColor2 -= len(self.colors)
		color2 = self.colors[iColor2]

		fraction2 = self.iColor - int(self.iColor)
		fraction1 = 1 - fraction2
		red = fraction1 * color1[0] + fraction2 * color2[0]
		green = fraction1 * color1[1] + fraction2 * color2[1]
		blue = fraction1 * color1[2] + fraction2 * color2[2]

		self.currentColor = (red, green, blue)
		return