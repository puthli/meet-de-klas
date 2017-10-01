#!/usr/bin/python
#
#   main.py
#   Reads sensor values and sends them to a server through LoRa
#   Requires LoPy with CoZIR CO2, Temperature and Humidity sensor attached
#   Version 1.0
#   Author R. Puthli, Itude Mobile
#
#
import sys
sys.path.append("/..")
import TTN
from machine import UART
from machine import Pin
import time
import socket
import binascii
import pycom
import LEDColors
from dth import DTH
import gc

print('Meet de Klas instructie 0.01.01')
gc.enable()

# stop the blue light from flickering
pycom.heartbeat(False)
led = LEDColors.pyLED()

print('Starting up...')

#setup LoRa connection
connection = TTN.LoRaConnection()
print("LoRa device EUI:")
connection.getDeviceEUI()
connection.start()

# setup sensor
pin = Pin('G7', mode=Pin.OPEN_DRAIN)
while True:
    th = DTH(pin,0)
    result = th.read()
    if result.is_valid():
        led.setLED('green')
    else:
        led.setLED('red')
    co2 = "00000" # no CO2 sensor in DHT11
    hum = "{0:0>2}0".format(result.humidity)
    temp = "{0:0>2}0".format(result.temperature)
    # release memory
    del(result)
    del(th)

    dataline = co2+hum+temp
    led.setLED('off')
    print(dataline)
    data = bytearray()
    for i in bytes(dataline, 'utf-8'):
        try:
            data.append(int(chr(i))) # convert ascii characters to bytes
        except ValueError:
            print("Non number in data - sensor is producing gibberish")
    connection.sendData(data)
    gc.collect()
    time.sleep(20)
