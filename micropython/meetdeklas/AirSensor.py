#   Class CoZIR
#   Wrapper for serial communication with CoZIR CO2, Temperature and Humidity sensor
#   Version 1.0
#   Author R. Puthli, Itude Mobile

class AirSensor():
    def setup(self):
        pass

    def turnOn(self):
        pass

    def turnOff(self):
        pass

    def getTemperature(self):
        return b'200'

    def getHumidity(self):
        return b'500'

    def getCO2(self):
        return b'00450'
