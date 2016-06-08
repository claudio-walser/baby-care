#!/usr/bin/env python3

from daemon import Daemon
import logging

PIDFILE = "/tmp/test.pid"
LOGFILE = "/tmp/daemon.log"
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
logging.captureWarnings(True)

class Daemon (Daemon):

  def run(self):
    # maybe i can fetch the cursor here, since i now i have to commit after a update, it might work :p
    while True:
      #accept connections from outside
      logging.debug('daemon is running')
