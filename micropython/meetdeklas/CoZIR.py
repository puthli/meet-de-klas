#   Class CoZIR
#   Wrapper for serial communication with CoZIR CO2, Temperature and Humidity sensor
#   Version 1.0
#   Author R. Puthli, Itude Mobile
#
#
from machine import UART
from machine import Pin
import time
from AirSensor import AirSensor


class CoZIR(AirSensor):
    # this uses the UART_1 with pins that do not conflict with the SD card
    # this equals G9 and G8 on the Pycom extension board
    # the UART definition is made for each writeCommand to eliminate conflicts
    # with other UART devices (e.g. pycom deep sleep shield)

    sensorWarmupInterval = 11 # seconds required for the CO2 sensor to warm up

    def writeCommand(self, command):
        output = command + '\r\n'
        uart = UART(1, baudrate=9600, pins=(Pin.exp_board.G9, Pin.exp_board.G8))
        uart.write(output)
        #wait max 3(s) for output from the sensor
        waitcounter = 0
        while (waitcounter < 5 and not uart.any()):
            time.sleep(0.5)
            waitcounter += 1
        response = uart.readall()
        uart.deinit()
        print(response)
        return(response)

    #returns a 5 byte parts per million value
    def getCO2(self):
        rawCO2 = self.writeCommand('Z')
        if (rawCO2 != None):
            CO2ppm = rawCO2[3:8]
            return CO2ppm

    #returns a 3 byte percentage. The last byte is a decimal
    def getHumidity(self):
        rawHumidity = self.writeCommand('H')
        if (rawHumidity != None):
            humidity = rawHumidity[5:8]
            return humidity

    #returns a 3 byte percentage. The last byte is a decimal
    def getTemperature(self):
        rawTemperature = self.writeCommand('T')
        if (rawTemperature != None):
            temperature = rawTemperature[5:8]
            return temperature

    def turnOn(self):
        self.writeCommand('K 2')
        time.sleep(self.sensorWarmupInterval) #let sensor warmup cyle finish

    def turnOff(self):
        self.writeCommand('K 0')

    # calibrates the CO2 sensor to 400 ppm.
    def calibrateCO2(self):
        self.writeCommand('G')

    # set digitalFilter for CO2 smoothing.
    # Filter setting 8 Requires 9(s) warmup in addition to 1.2(s)
    # for the power cycle.
    def setDigitalFilter(self):
        self.writeCommand('A 8')

    def setup(self):
        self.setDigitalFilter()
