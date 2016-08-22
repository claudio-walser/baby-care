import socket

class SurveillanceStatus (object):

    socket = False
    host = '10.20.1.98'
    port = 8080

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def activate(self):
        # listen on main port for game input
        self.socket.send('set status acitve')

    def deactivate(self):
        self.socket.send('set status inactive')

    def getStatus(self):
        self.socket.send('get status')