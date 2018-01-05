#!/usr/bin/python
#   Class SDCardLogger
#   Version 0.1

from machine import SD
import os
import time


class SDLogger:

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
        text = 'INFO, %s, %s' % (time.time(), line)
        print(text)
        self.append('log.txt', text)

    def logError(self, line):
        text = 'ERROR, %s, %s' % (time.time(), line)
        print(text)
        self.append('log.txt', text)
