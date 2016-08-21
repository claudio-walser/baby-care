import grovepi
from surveillance.Sensors.Sensor import Sensor

class Grove (Sensor):

	def setup(self):
		grovepi.pinMode(self.airQualitySensor, "INPUT")
		return True

	def readTemperature(self):
		self.readGroveValues()
		return self.temperature

	def readHumidity(self):
		self.readGroveValues()
		return self.humidity

	def readAirQuality(self):
		self.readGroveValues()
		return self.airQuality
