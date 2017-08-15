#   Class TTNConnection
#   Wrapper for LoRaWan communication with The Things Network
#   Version 1.0
#   Author R. Puthli, Itude Mobile
#
#
from network import LoRa
import socket
import time
import binascii
import pycom
import LEDColors


class LoRaConnection:
    # Initialize LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN)

    def start(self):
        # create an OTAA authentication parameters, do NOT change these
        app_eui = binascii.unhexlify('70B3D57EF00068A4'.replace(' ', ''))
        app_key = binascii.unhexlify('F132D8E3289C14386E78C6253B16F641'.replace(' ', ''))

        # join a network using OTAA (Over the Air Activation)
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        pycom.rgbled(LEDColors.color['pink'])
        # wait until the module has joined the network
        while not self.lora.has_joined():
            pycom.rgbled(LEDColors.color['purple'])
            time.sleep(0.5)
            pycom.rgbled(LEDColors.color['off'])
            time.sleep(2.0)
            print('Not yet joined...')
        # display that the module has joined the network
        print('Joined!')
        pycom.rgbled(LEDColors.color['blue'])
        time.sleep(1)
        pycom.rgbled(LEDColors.color['off'])
        return self.lora

    def sendData(self, data):
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)
        pycom.rgbled(LEDColors.color['blue'])
        s.send(data)
        pycom.rgbled(LEDColors.color['off'])
        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)
        # get any data received and print if there is any
        data = s.recv(64)
        if len(data) > 0:
            print(data)

    # needed to fill in the TTN console
    def getDeviceEUI(self):
        print(binascii.hexlify(self.lora.mac()).upper().decode('utf-8'))
