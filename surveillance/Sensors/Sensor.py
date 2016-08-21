import grovepi
import time

class Sensor (object):

	dhtSensor = 4
	dhtSensorType = 1

	airQualitySensor = 0

	lastTime = 0
	
	temperature = 0
	humidity = 0
	airQuality = 0

	def setup(self):
		return True

	def readGroveValues(self):
		if time.time() - self.lastTime > 0.5:
			lastTime = time.time()
			[self.temperature, self.humidity] = grovepi.dht(self.dhtSensor, self.dhtSensorType)
			#self.airQuality = 'NaN'
			self.airQuality = grovepi.analogRead(self.airQualitySensor)
