#!/usr/bin/env python3

import audioop
import pyaudio
import time

from pprint import pprint

chunk = 1024
volumeTreshold = 1024
deviceIndex = 1
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


noiseStarted = False
startTime = 0;

while 1:
  currentTime = time.time()

  data = stream.read(chunk)
  rms = audioop.rms(data, 2)  #width=2 for format=paInt16
  if rms >= volumeTreshold:
    if noiseStarted == False:
      noiseStarted = True
      startTime = time.time()
    else:
      timeDiff = currentTime - startTime
      print("time started: %s " % startTime)
      print("current detection: %s " % time.time())
      print("time diff since noise started: %s " % timeDiff)
      if timeDiff >= alarmingTreshold:
        print("Alarm Alarm")

    print(rms)

  else:
    if noiseStarted == True:
      timeDiff = currentTime - startTime
      if timeDiff > acceptablePause:
        noiseStarted = False
        startTime = 0

