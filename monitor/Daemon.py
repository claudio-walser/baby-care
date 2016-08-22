#!/usr/bin/env python3

from daemon import Daemon
import logging
import time
import socket
import json


from pprint import pprint

class Daemon (Daemon):

  port = 8082
  host = '10.20.1.98'
  socket = False

  def setLogging(self, logging: logging):
    self.logging = logging
  
  def run(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen on main port for game input
    self.socket.connect((self.host, self.port))
    
    (connection, address) = self.socket.accept()
    data = True
    while data:
      data = connection.recv(4096)
      self.process(json.loads(data))


  def process(self, data):
    pprint(data)
    self.logging.debug("Data was being sent: %s" % data)
