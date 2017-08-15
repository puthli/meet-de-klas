#!/usr/bin/python
#
#   main.py
#   Reads sensor values and sends them to a server through LoRa
#   Requires LoPy with CoZIR CO2, Temperature and Humidity sensor attached
#   Version 1.0
#   Author R. Puthli, Itude Mobile
#
#
import TTN
from machine import UART
import time
import socket
import binascii
import pycom
import CoZIR
import LEDColors


print('Starting up...')
############################################################################
#setup sensor
coZIR = CoZIR.CoZIR()
coZIR.setModeLowPower()
coZIR.calibrateCO2()

#stop the blue light from flickering
pycom.heartbeat(False)

############################################################################
#setup LoRa connection
connection = TTN.LoRaConnection()
connection.start()

############################################################################
#main execution looop
minutes = 1 # number of minutes to wait between polling the sensor and sending
CO2warninglevel = 100
CO2dangerlevel = 1400
while 1:
    pycom.rgbled(LEDColors.color['purple'])
    coZIR.setModePolling()
    time.sleep(10) #let sensor warmup cyle finish
    co2 = coZIR.getCO2()
    hum = coZIR.getHumidity()
    temp = coZIR.getTemperature()
    dataline = co2+hum+temp
    pycom.rgbled(LEDColors.color['off'])
    coZIR.setModeLowPower()
    print(dataline)
    data = bytearray()
    for i in dataline:
        data.append(int(chr(i))) # convert ascii characters to bytes
    connection.sendData(data)

    co2int = int(co2)
    if(co2int>CO2dangerlevel):
        pycom.rgbled(LEDColors.color['red'])
    if(co2int>CO2warninglevel):
        pycom.rgbled(LEDColors.color['orange'])

    time.sleep(60*minutes)
