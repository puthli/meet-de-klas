# !/usr/bin/python
#
#   main.py
#   Reads sensor values and sends them to a server through LoRa
#   Requires LoPy with CoZIR CO2, Temperature and Humidity sensor attached
#   Version 0.11.02
#   Author R. Puthli, Itude Mobile
#
#
import TTN
import time
import pycom
from AirSensor import AirSensor
from CoZIR import CoZIR
import LEDColors
from network import WLAN
from SDCardUtils import SDLogger
import machine

sd = SDLogger()

SENSORERRORCODE = b'99'
normalSleepTime = 15 # in minutes
panicSleepTime = 15 # in minutes
co2PanicLevel = 1000 # ppm level above which is unhealthy
highTempPanicLevel = 260 # degrees centigrade above which is unhealthy (includes a decimal)
lowTempPanicLevel = 150 # degrees centigrade below which is unhealthy (includes a decimal)
sd.logInfo('Okku version 0.11.02')

# stop the blue light from flickering
pycom.heartbeat(False)
led = LEDColors.pyLED()
# disable WiFi
wlan = WLAN()
wlan.deinit()


connection = TTN.LoRaConnection()
#airSensor = AirSensor()
airSensor = CoZIR()
sd.logInfo(machine.reset_cause())
if (machine.reset_cause() != machine.DEEPSLEEP_RESET): # if power on bit set
    sd.logInfo('Starting up...')
    ############################################################################
    # setup sensor
    airSensor.turnOff()
    airSensor.setup()

    # calibrate CO2
    sd.logInfo('Calibrating CO2...')
    airSensor.turnOn()
    airSensor.calibrateCO2()

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
sd.logInfo("Let sensor warm up...")
airSensor.turnOn()
co2 = airSensor.getCO2()
hum = airSensor.getHumidity()
temp = airSensor.getTemperature()
airSensor.turnOff()

#   write to SD card in format (LoRa EUI, time(s), dataline)
sd.append('%s.csv' % connection.lora.mac(), '%s, %s, %s, %s' % (time.time(), co2, temp, hum))
#   create data for LoRa Message
try:
    dataline = co2+hum+temp
    if (int(co2) > co2PanicLevel or int(temp) > highTempPanicLevel or int(temp) < lowTempPanicLevel):
        # start blurting out signals at a higher rate
        sd.logInfo("Panic mode, setting shorter sleep interval: %d minutes" % panicSleepTime)
        minutes = panicSleepTime
    else:
        sd.logInfo("Normal mode, setting sleep interval: %d minutes" % normalSleepTime)
        minutes = normalSleepTime
except TypeError:
    dataline = SENSORERRORCODE

sd.setProperty('lastSensorValues', dataline)
led.setLED('off')
sd.logInfo(dataline)
data = bytearray()
for i in dataline:
    try:
        data.append(int(chr(i))) # convert ascii characters to bytes
    except ValueError:
        sd.logInfo("Non number in data - sensor is producing gibberish")

connection.sendData(data)
connection.lora.nvram_save()

# machine.deepsleep(20*1000) # milliseconds
machine.deepsleep(1000*60*minutes)
