# baby-care

Baby phone using two raspberry pi's. One used as surveillance device, sitting in the baby room. The other as monitoring/alarming device in the parents room.
No wireless radiation because they are connected over power-lan. Very secure because they are not conntected to the internet.


Its using VLC Player to create a live stream from the webcam and pyaudio for noise detection. If noise is detected for 30 seconds with a max pause of 5 seconds, alarming is starting.

# installation prerequisites

apt-get install vlc
pip3 install pyaudio