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
from network import WLAN
import gc

print('Meet de Klas version 0.08.01')
gc.enable()

# stop the blue light from flickering
pycom.heartbeat(False)
led = LEDColors.pyLED()
# disable WiFi
wlan = WLAN()
wlan.deinit()

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
    coZIR.setDigitalFilter()

    #setup LoRa connection
    connection.start()
    connection.lora.nvram_save()
else:
    print('Woken up after deep sleep timer expired')
    connection.lora.nvram_restore() # restore saved LoRa connection

############################################################################
#main execution loop, triggered by awakening from deep sleep
minutes = 1 # number of minutes to wait between polling the sensor and sending
led.setLED('green')
coZIR.setModePolling()
print("Let sensor warm up...")
time.sleep(7) #let sensor warmup cyle finish
co2 = coZIR.getCO2()
hum = coZIR.getHumidity()
temp = coZIR.getTemperature()
dataline = co2+hum+temp
led.setLED('off')
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
sleep = DeepSleep.DeepSleep()
gc.collect()
sleep.go_to_sleep(60*minutes)
