#!/usr/bin/env python3

import audioop
import pyaudio

from pprint import pprint

chunk = 1024
volumeTreshold = 1024

p = pyaudio.PyAudio()

print(p.get_device_count())
pprint(p.get_device_info_by_index(2))

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=32000,
                input=True,
                input_device_index = 2,
                frames_per_buffer=chunk)

while 1:
  data = stream.read(chunk)
  rms = audioop.rms(data, 2)  #width=2 for format=paInt16
  if rms >= volumeTreshold:
    print(rms)

