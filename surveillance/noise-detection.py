#!/usr/bin/env python3

import audioop
import pyaudio
import time

from pprint import pprint

chunk = 1024
volumeTreshold = 1024
deviceIndex = 2
# time in seconds of noise detection until alarming the monitoring device
alarmingTreshold = 30
# time in seconds for an acceptable pause which is not interrupting the alarmingTreshold
acceptablePause = 5


p = pyaudio.PyAudio()


pprint(p.get_device_info_by_index(deviceIndex))


stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                input=True,
                input_device_index = deviceIndex,
                frames_per_buffer=chunk)

noiseStartedTime = 0
silenceStartedTime = 0

while 1:
  currentTime = time.time()

  data = stream.read(chunk)
  rms = audioop.rms(data, 2)  #width=2 for format=paInt16
  if rms >= volumeTreshold:
    silenceStartedTime = 0
    if noiseStartedTime == 0:
      noiseStartedTime = currentTime
    else:
      noiseDiff = currentTime - noiseStartedTime
      print("noise since: %s " % noiseDiff)
      if noiseDiff >= alarmingTreshold:
        print("Alarm Alarm")

    print(rms)

  else:
    if noiseStartedTime > 0:
      if silenceStartedTime == 0:
        silenceStartedTime = currentTime

      silenceDiff = currentTime - silenceStartedTime
      print("silence since: %s " % silenceDiff)
      if silenceDiff > acceptablePause:
        noiseStartedTime = 0

