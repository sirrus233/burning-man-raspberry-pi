from TPack import TPack
from TBike import TBike


# Pick what configuration we're in
# 1 = pack
# 2 = Bike
conf = 1

# Options
dimmer = 0
packAnimation = 1
packCycleTime = 60



# Let's do it
if conf == 1:
	pack = TPack(dimmer, packAnimation, packCycleTime)
	pack.run()
elif conf == 2:
	bike = TBike(dimmer)
	bike.run()