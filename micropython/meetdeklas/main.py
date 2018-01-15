#!/usr/bin/python
#
#   main.py
#   Reads sensor values and sends them to a server through LoRa
#   Requires LoPy with CoZIR CO2, Temperature and Humidity sensor attached
#   Version 0.10.02
#   Author R. Puthli, Itude Mobile
#
#
import TTN
import time
import pycom
import CoZIR
import LEDColors
from network import WLAN
import SDCardUtils
import machine

sd = SDCardUtils.SDLogger()

normalSleepTime = 30 # in minutes
panicSleepTime = 5 # in minutes
co2PanicLevel = 1000 # ppm level above which is unhealthy
highTempPanicLevel = 260 # degrees centigrade above which is unhealthy (includes a decimal)
lowTempPanicLevel = 150 # degrees centigrade below which is unhealthy (includes a decimal)
sensorWarmupInterval = 7 # seconds required for the CO2 sensor to warm up
sd.logInfo('Meet de Klas version 0.10.02')

# stop the blue light from flickering
pycom.heartbeat(False)
led = LEDColors.pyLED()
# disable WiFi
wlan = WLAN()
wlan.deinit()


connection = TTN.LoRaConnection()
coZIR = CoZIR.CoZIR()
sd.logInfo(machine.reset_cause())
if (machine.reset_cause() != machine.DEEPSLEEP_RESET): # if power on bit set
    sd.logInfo('Starting up...')
    ############################################################################
    # setup sensor
    coZIR.setModePolling()
    sd.logInfo("Let sensor warm up...")
    time.sleep(sensorWarmupInterval) #let sensor warmup cyle finish
    coZIR.calibrateCO2()
    time.sleep(2) #let calibration finish
    coZIR.setModeLowPower()
    coZIR.setDigitalFilter()

    #setup LoRa connection
    sd.logInfo("Device EUI: %s" % connection.getDeviceEUI())
    connection.start()
    connection.lora.nvram_save()
else:
    sd.logInfo('Woken up after deep sleep timer expired')
    connection.lora.nvram_restore() # restore saved LoRa connection

############################################################################
#main execution loop, triggered by awakening from deep sleep
minutes = normalSleepTime # number of minutes to wait between polling the sensor and sending
led.setLED('green')
coZIR.setModePolling()
sd.logInfo("Let sensor warm up...")
time.sleep(sensorWarmupInterval) #let sensor warmup cyle finish
co2 = coZIR.getCO2()
hum = coZIR.getHumidity()
temp = coZIR.getTemperature()
#   write to SD card in format (LoRa EUI, time(s), dataline)
sd.append('%s.csv' % connection.lora.mac(), '%s, %s, %s, %s' % (time.time(), co2, temp, hum))
#   create data for LoRa Message
dataline = co2+hum+temp
sd.setProperty('lastSensorValues', dataline)
led.setLED('off')
coZIR.setModeLowPower()
sd.logInfo(dataline)
data = bytearray()
for i in dataline:
    try:
        data.append(int(chr(i))) # convert ascii characters to bytes
    except ValueError:
        sd.logInfo("Non number in data - sensor is producing gibberish")

connection.sendData(data)
connection.lora.nvram_save()

sleep = DeepSleep.DeepSleep()
if (int(co2) > co2PanicLevel or int(temp) > highTempPanicLevel or int(temp) < lowTempPanicLevel):
    # start blurting out signals at a higher rate
    sd.logInfo("Panic mode, setting shorter sleep interval: %d minutes" % panicSleepTime)
    minutes = panicSleepTime
else:
    sd.logInfo("Normal mode, setting sleep interval: %d minutes" % normalSleepTime)
    minutes = normalSleepTime

machine.deepsleep(20*1000) # milliseconds
#  machine.deepsleep(1000*60*minutes)
