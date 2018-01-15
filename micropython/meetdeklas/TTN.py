#!/usr/bin/python
#   Class TTNConnection
#   Wrapper for LoRaWan communication with The Things Network
#   Version 1.0.1
#   Author R. Puthli, Itude Mobile
#
#
from network import LoRa
import socket
import time
import binascii
import pycom
import LEDColors
import SDCardUtils

class LoRaConnection:
    # Initialize LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN)
    led = LEDColors.pyLED()

    def start(self):
        sd = SDCardUtils.SDLogger()

        # create an OTAA authentication parameters, do NOT change these
        app_eui = binascii.unhexlify('70B3D57EF00068A4'.replace(' ', ''))
        app_key = binascii.unhexlify('F132D8E3289C14386E78C6253B16F641'.replace(' ', ''))

        # join a network using OTAA (Over the Air Activation)
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        self.led.setLED('pink')
        # wait until the module has joined the network
        while not self.lora.has_joined():
            self.led.setLED('purple')
            time.sleep(0.5)
            self.led.setLED('off')
            time.sleep(2.0)
            sd.logInfo('Not yet joined...')
        # display that the module has joined the network
        sd.logInfo('Joined!')
        self.led.setLED('blue')
        time.sleep(1)
        self.led.setLED('off')
        return self.lora

    def sendData(self, data):
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3) # set the LoRaWAN data rate
        # s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, True) # use confirmed message
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)
        try:
            self.led.setLED('blue')
            s.send(data)
            self.led.setLED('off')
            # make the socket non-blocking
            # (because if there's no data received it will block forever...)
            s.setblocking(False)
            s.settimeout(3.0)
            # configure a timeout value of 3 seconds
            # get any data received and print if there is any
            data = s.recv(64)
            if len(data) > 0:
                print(data)
        except OSError as e:
            sd = SDCardUtils.SDLogger()
            sd.logInfo(e)

    # needed to fill in the TTN console
    def getDeviceEUI(self):
        return binascii.hexlify(self.lora.mac()).upper().decode('utf-8')
