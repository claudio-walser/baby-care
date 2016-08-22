#!/usr/bin/env python3

from daemon import Daemon
import sys
import time
import logging
from monitor.Daemon import Daemon as MonitorDaemon


PIDFILE = '/var/run/monitor.pid'
LOGFILE = '/var/log/monitor.log'

# Configure logging
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
logging.captureWarnings(True)


if __name__ == "__main__":

  daemon = MonitorDaemon(PIDFILE)
  daemon.setLogging(logging)
  if len(sys.argv) == 2:

    if 'start' == sys.argv[1]:
      try:
        daemon.start()
      except:
        pass

    elif 'stop' == sys.argv[1]:
      print('Stopping ...')
      daemon.stop()

    elif 'restart' == sys.argv[1]:
      print('Restaring ...')
      daemon.restart()

    elif 'status' == sys.argv[1]:
      try:
        pf = open(PIDFILE,'r')
        pid = int(pf.read().strip())
        pf.close()
      except IOError:
        pid = None
      except SystemExit:
        pid = None

      if pid:
        print('MonitorDaemon is running as pid %s' % pid)
      else:
        print('MonitorDaemon is not running.')

    else:
      print('Unknown command')
      sys.exit(2)
      sys.exit(0)
  else:
    print('usage: %s start|stop|restart|status' % sys.argv[0])
    sys.exit(2)
