#   Class CoZIR
#   Wrapper for serial communication with CoZIR CO2, Temperature and Humidity sensor
#   Version 1.0
#   Author R. Puthli, Itude Mobile
#
#
from machine import UART
import time


class CoZIR:
    uart = UART(1, baudrate=9600)
    # this uses the UART_1 default pins for TXD and RXD (``P3`` and ``P4``)
    # this equals G11 and G24 on the Pycom extension board

    def writeCommand(self, command):
        output = command + '\r\n'
        self.uart.write(output)
        #wait max 3(s) for output from the sensor
        waitcounter = 0
        while (waitcounter < 5 and not self.uart.any()):
            time.sleep(0.5)
            waitcounter += 1
        response = self.uart.readall()
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

    def setModePolling(self):
        self.writeCommand('K 2')

    def setModeLowPower(self):
        self.writeCommand('K 0')

    #calibrates the CO2 sensor to 400 ppm.
    def calibrateCO2(self):
        self.writeCommand('G')
