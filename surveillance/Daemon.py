#!/usr/bin/env python3

from daemon import Daemon
import logging
import time
import socket
import json

from surveillance.Video import Video

from surveillance.Sensors.Audio import Audio
from surveillance.Sensors.Grove import Grove

from pprint import pprint

class Daemon (Daemon):

  port = 8082
  host = '10.20.1.98'
  socket = False

  volumeTreshold = 32
  # time in seconds of noise detection until alarming the monitoring device
  alarmingTreshold = 10
  # time in seconds for an acceptable pause which is not interrupting the alarmingTreshold
  acceptablePause = 5


  alarming = True
  noiseStartedTime = 0
  silenceStartedTime = 0

  statusFile = "/home/baby-care/baby-care/surveillance-status"
  status = 'active'


  def setLogging(self, logging: logging):
    self.logging = logging
  
  def run(self):
    video = Video()

    sensorGrove = Grove()
    sensorGrove.setup()

    sensorAudio = Audio()
    sensorAudio.setup()

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen on main port for game input
    self.socket.bind((self.host, self.port))
    self.socket.listen(5)

    while True:

      try:
        video.run()
        self.readStatus()

        humidity = sensorGrove.readHumidity()
        temperature = sensorGrove.readTemperature()
        airQuality = sensorGrove.readAirQuality()
        volume = sensorAudio.readVolume()
        isAlarm = self.isAlarming(volume)

        info = {
          'status': self.status,
          'isAlarm': isAlarm,
          'volume': volume,
          'temperature': temperature,
          'humidity': humidity,
          'airQuality': airQuality
        }
        self.socket.send(json.dump(info))
        self.logging.debug(info)

      except Exception as e:
        logging.error(e)

  def readStatus(self):
    f = open(self.statusFile, 'rb')
    self.status = f.read().decode("utf-8").strip()
    f.close()

  def startAlarming(self):
    self.alarming = True

  def stopAlarming(self):
    self.noiseStartedTime = 0
    self.silenceStartedTime = 0
    self.alarming = False


  def isAlarming(self, volume):
    if self.status == "inactive":
      if not self.alarming == False:
        self.stopAlarming()
      return False
    else:
      if self.alarming == False:
        self.startAlarming()

    currentTime = time.time()


    if volume >= self.volumeTreshold:
      self.silenceStartedTime = 0
      if self.noiseStartedTime == 0:
        self.noiseStartedTime = currentTime
      else:
        noiseDiff = currentTime - self.noiseStartedTime
        #self.logging.debug("noise since: %s " % noiseDiff)
        if noiseDiff >= self.alarmingTreshold:
          return True
    else:
      if self.noiseStartedTime > 0:
        if self.silenceStartedTime == 0:
          self.silenceStartedTime = currentTime

        silenceDiff = currentTime - self.silenceStartedTime
        #self.logging.debug("silence since: %s " % silenceDiff)
        if silenceDiff > self.acceptablePause:
          self.noiseStartedTime = 0
    return False
