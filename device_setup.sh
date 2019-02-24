#!/bin/bash

sudo mkdir /opt/presentation ; \
sudo cp config.py /opt/presentation ; \
sudo cp app.py /opt/presentation ; \
sudo cp power_generator_sensehat.py /opt/presentation

sudo apt update

sudo apt install -y python3-pip

pip3 --version


sudo apt-get install wiringpi

# gpio -g mode 18 out
# gpio -g write 18 1
# gpio -g write 18 0



sudo pip3 install RPi.Gpio



sudo apt-get install libboost-python1.62.0

sudo pip3 install azure-iothub-device-client


sudo apt-get install -yq \
python sense-hat raspberrypi-bootloader && \
apt-get clean && rm -rf /var/lib/apt/lists/*
