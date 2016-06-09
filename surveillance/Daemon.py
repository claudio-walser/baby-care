#!/usr/bin/env python3

from daemon import Daemon
import logging
import audioop
import pyaudio
import time

from pprint import pprint

class Daemon (Daemon):

  audio = False
  stream = False
  chunk = 1024
  volumeTreshold = 16
  deviceIndex = 0
  # time in seconds of noise detection until alarming the monitoring device
  alarmingTreshold = 30
  # time in seconds for an acceptable pause which is not interrupting the alarmingTreshold
  acceptablePause = 5


  noiseStartedTime = 0
  silenceStartedTime = 0

  statusFile = "/Users/walsercl/Development/claudio/baby-care/surveillance/status"

  def setLogging(self, logging: logging):
    self.logging = logging

  def run(self):

    self.audio = pyaudio.PyAudio()

    self.logging.debug(self.audio.get_device_info_by_index(self.deviceIndex))
    self.stream = self.audio.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                input=True,
                input_device_index = self.deviceIndex,
                frames_per_buffer = self.chunk)
    
    # maybe i can fetch the cursor here, since i now i have to commit after a update, it might work :p
    while True:
      with open(self.statusFile, "rb") as f:
        status = f.read().strip()
      #accept connections from outside
      self.logging.debug(status)
      self.listen(status)
        

  def reset(self):
    self.noiseStartedTime = 0
    self.silenceStartedTime = 0

  def listen(self, status: str):
    if status == "inactive":
      self.reset()
      self.logging.debug("inactive")
      return False


    currentTime = time.time()

    data = self.stream.read(self.chunk)
    rms = audioop.rms(data, 2)  #width=2 for format=paInt16
    if rms >= self.volumeTreshold:
      self.silenceStartedTime = 0
      if self.noiseStartedTime == 0:
        self.noiseStartedTime = currentTime
      else:
        noiseDiff = currentTime - self.noiseStartedTime
        self.logging.debug("noise since: %s " % noiseDiff)
        if noiseDiff >= self.alarmingTreshold:
          self.logging.debug("Alarm Alarm")

      self.logging.debug(rms)

    else:
      if self.noiseStartedTime > 0:
        if self.silenceStartedTime == 0:
          self.silenceStartedTime = currentTime

        silenceDiff = currentTime - self.silenceStartedTime
        self.logging.debug("silence since: %s " % silenceDiff)
        if silenceDiff > self.acceptablePause:
          self.noiseStartedTime = 0

