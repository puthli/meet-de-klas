#!/usr/bin/python
#
#   main.py
#   Reads sensor values and sends them to a server through LoRa
#   Requires LoPy with CoZIR CO2, Temperature and Humidity sensor attached
#   Version 0.10.01
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

normalSleepTime = 30 # in minutes
panicSleepTime = 5 # in minutes
co2PanicLevel = 1000 # ppm level above which is unhealthy
highTempPanicLevel = 260 # degrees centigrade above which is unhealthy (includes a decimal)
lowTempPanicLevel = 150 # degrees centigrade below which is unhealthy (includes a decimal)
sensorWarmupInterval = 7 # seconds required for the CO2 sensor to warm up
print('Meet de Klas version 0.10.01')
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
    coZIR.setModePolling()
    print("Let sensor warm up...")
    time.sleep(sensorWarmupInterval) #let sensor warmup cyle finish
    coZIR.calibrateCO2()
    time.sleep(2) #let calibration finish
    coZIR.setModeLowPower()
    coZIR.setDigitalFilter()

    #setup LoRa connection
    print("Device EUI:")
    connection.getDeviceEUI()
    connection.start()
    connection.lora.nvram_save()
else:
    print('Woken up after deep sleep timer expired')
    connection.lora.nvram_restore() # restore saved LoRa connection

############################################################################
#main execution loop, triggered by awakening from deep sleep
minutes = normalSleepTime # number of minutes to wait between polling the sensor and sending
led.setLED('green')
coZIR.setModePolling()
print("Let sensor warm up...")
time.sleep(sensorWarmupInterval) #let sensor warmup cyle finish
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
if (int(co2) > co2PanicLevel or int(temp) > highTempPanicLevel or int(temp) < lowTempPanicLevel):
    # start blurting out signals at a higher rate
    print("Panic mode, setting shorter sleep interval: %d minutes" % panicSleepTime)
    minutes = panicSleepTime
else:
    print("Normal mode, setting sleep interval: %d minutes" % normalSleepTime)
    minutes = normalSleepTime

gc.collect()
sleep.go_to_sleep(60*minutes)
