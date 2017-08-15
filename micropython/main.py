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
import DeepSleep

#stop the blue light from flickering
pycom.heartbeat(False)

connection = TTN.LoRaConnection()
coZIR = CoZIR.CoZIR()
sleep = DeepSleep.DeepSleep()
print(sleep.get_wake_status())
if (sleep.get_wake_status()["wake"] >> 5 == 1): # if power on bit set
    print('Starting up...')
    ############################################################################
    # setup sensor
    coZIR.setModeLowPower()
    coZIR.calibrateCO2()

    #setup LoRa connection
    connection.start()
    connection.lora.nvram_save()
else:
    print('Woken up after deep sleep timer expired')
    connection.lora.nvram_restore() # restore saved LoRa connection

############################################################################
#main execution loop, triggered by awakening from deep sleep
minutes = 1 # number of minutes to wait between polling the sensor and sending
CO2warninglevel = 100
CO2dangerlevel = 1400
while 1:
    pycom.rgbled(LEDColors.color['purple'])
    coZIR.setModePolling()
    print("Let sensor warm up...")
    time.sleep(15) #let sensor warmup cyle finish
    co2 = coZIR.getCO2()
    hum = coZIR.getHumidity()
    temp = coZIR.getTemperature()
    dataline = co2+hum+temp
    pycom.rgbled(LEDColors.color['off'])
    coZIR.setModeLowPower()
    print(dataline)
    data = bytearray()
    for i in dataline:
        try:
            data.append(int(chr(i))) # convert ascii characters to bytes
        except ValueError:
            print("Non number in data - sensor is producing gibberish")
    connection.sendData(data)
    connection.lora.nvram_save()

    # co2int = int(co2)
    # if(co2int>CO2dangerlevel):
    #     pycom.rgbled(LEDColors.color['red'])
    # if(co2int>CO2warninglevel):
    #     pycom.rgbled(LEDColors.color['orange'])

# sleep.go_to_sleep(10)
