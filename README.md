# LED-RaspberryPi-Python

This is example how to communicate with IoTHub from Raspberry PI A+. I built it based on this great example https://github.com/Azure-Samples/iot-hub-python-raspberrypi-client-app, compared with some other I tried, that just worked. During setup.sh process it failed with memory problems, but the code still worked. Before that I ran this

sudo apt-get install libboost-python1.62.0
sudo pip3 install azure-iothub-device-client

The libboost was due to some problems I had on my computer with ubuntu 18.04. I found somewhere to run libboost first, didn't help on my OS, but worked on Raspberry PI. You can try to run first those two commands and then python code without setup.sh, if it doesn't work, do setup.

The device will operate LED based on "turn on", "turn off" commands from IotHub.
