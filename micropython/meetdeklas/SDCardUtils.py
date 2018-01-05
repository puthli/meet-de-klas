#!/usr/bin/python
#   Class SDCardLogger
#   Version 0.1

from machine import SD
from machine import RTC
import os
import time


class SDLogger:

    # get a key, value pair
    def getProperty(self, key):
        result = None
        # mount SD if not mounted already
        try:
            sd = SD()
            try:
                os.mount(sd, '/sd')
            except OSError:
                pass
                # SD card already mounted

            try:
                with open('/sd/property_%s' % key, 'r') as file:
                    result = file.read()
            except OSError as e:
                print(e)
        except OSError:
            print('SD card cannot be written to')
        return result

    # store a key, value pair
    def setProperty(self, key, value):
        # mount SD if not mounted already
        try:
            sd = SD()
            try:
                os.mount(sd, '/sd')
            except OSError:
                pass
                # SD card already mounted

            try:
                with open('/sd/property_%s' % key, 'w') as file:
                    file.write('%s' % value)
            except OSError as e:
                print(e)
        except OSError:
            print('SD card cannot be written to')

    # append a line to a file on the SD card
    def append(self, filename, line):
        # mount SD if not mounted already
        try:
            sd = SD()
            try:
                os.mount(sd, '/sd')
            except OSError:
                pass
                # SD card already mounted

            try:
                with open('/sd/%s' % filename, 'a') as file:
                    file.write('%s\n' % line)
            except OSError as e:
                print(e)
        except OSError:
            print('SD card cannot be written to')

    # view a file on the SD card from REPL
    def view(self, filename):

        # mount SD if not mounted already
        sd = SD()
        try:
            os.mount(sd, '/sd')
        except OSError:
                pass
                # SD card already mounted

        try:
            with open('/sd/%s' % filename, 'r') as file:
                for line in file:
                    print(line,)
        except OSError as e:
            print(e)

    def logInfo(self, line):
        rtc = RTC()

        text = 'INFO, %s, %s' % (time.time(), line)
        print(text)
        self.append('log.txt', text)

    def logError(self, line):
        text = 'ERROR, %s, %s' % (time.time(), line)
        print(text)
        self.append('log.txt', text)
