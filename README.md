# LED-RaspberryPi-Python

This is example how to communicate with IoTHub from Raspberry PI A+. I built it based on this great example https://github.com/Azure-Samples/iot-hub-python-raspberrypi-client-app, compared with some other I tried, that just worked. During setup.sh process it failed with memory problems, but the code still worked. Before that I ran this

sudo apt-get install libboost-python1.62.0
sudo pip3 install azure-iothub-device-client

The libboost was due to some problems I had on my computer with ubuntu 18.04. I found somewhere to run libboost first, didn't help on my OS, but worked on Raspberry PI. You can try to run first those two commands and then python code without setup.sh, if it doesn't work, do setup.

The device will operate LED based on "turn on", "turn off" commands from IotHub.

## How to set up Raspberry Pi

I run it on Raspberry Pi 3 recently. I burned on SD card raspbian-stretch-lite, I was running it headless so I added ssh file and wpa_supplicant.conf to SD card to connect after starting to WiFi and enable ssh. ssh file is empty and in wpa_supplicant you have to replace ssid with WiFi name and psk with WiFi password.

After starting Raspberry Pi, you should be able to find it, I run this command on Linux to see all connected devices. Replace IP with your computers IP.

```
nmap -sn 192.168.0.1/24
```

You should see all devices, try to find Raspberry Pi. Once it's there you can ssh to it

```
ssh pi@192.168.0.1
```

Default Raspbian password is raspberry. Once you are sucesfully connected, you can run copyFiles.sh, replace Ip and password inside script before running the script. It should copy necessary files to device.

Go back to tab with ssh connection, run ls to see if all scripts are there. If they are, run device_setup.sh it should install all essential things on RPi. When it's done you can run one of two programs - either app.py or power_generator_sensehat.py

If you want to run code after start of RPi, add one of two lines into /etc/rc.local before exit 0

You can run RPI with Sense Hat -

```
python3 /opt/presentation/power_generator_sensehat.py 'paste here device connection string' 0 &
```

For device with LED run

```
python3 /opt/presentation/app.py 'paste here device connection string' &
```
