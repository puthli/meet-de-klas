# Micropython code for pycom LoPy with attached CoZIR CO2, Humidity and Temperature sensor

To use this code you need:
- a LoPy board, pycom deep sleep shield, pycom expansion board, CoZIR-AH sensor, attached LoRa antenna (make sure: no antenna = fried LoRa chip)
- the pymakr plugin (for Atom or other editor)

Update the LoPy firmware before you start (consult pycom.io for the latest updater program)

The hardware setup to connect the CO2 sensor is in ../hardware

The pycom deep sleep shield is a hardware shield provided with pycom LoPy boards. It can be requested free of charge from pycom for existing (older) LoPy's.

Code to use an alternative, cheaper DHT11 sensor is in the instruction folder.
