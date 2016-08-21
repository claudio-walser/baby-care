from surveillance.Sensors.Sensor import Sensor

import audioop
import pyaudio

class Audio (Sensor):

	chunk = 1024
	deviceIndex = 2
	
	def readVolume(self):
		audio = pyaudio.PyAudio()
		stream = audio.open(format=pyaudio.paInt16,
			channels=1,
			rate=32000,
			input=True,
			input_device_index = self.deviceIndex,
			frames_per_buffer = self.chunk)		

		data = stream.read(self.chunk)
		volume = audioop.rms(data, 2)  #width=2 for format=paInt16

		stream.close()

		return volume
