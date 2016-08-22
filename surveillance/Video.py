import subprocess


class Video (object):

  process = False
  command = 'cvlc v4l2:///dev/video0:width=480:height=320 \
  :v4l2-standard= \
  :input-slave=alsa://plughw:1,0 \
  :live-caching=300 \
  :sout="#transcode{\
    # vcodec=WMV2,\
    vb=800,\
    scale=1,\
    acodec=wma2,\
    ab=128,\
    channels=2,\
    samplerate=44100\
  }:http{dst=:8080/stream.wmv}"'


  def run(self):
    if self.process is False or self.process.poll() is not None:
      self.process = subprocess.Popen(self.command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
