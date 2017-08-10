#LED colors
color = {'off': 0x000000, 'red':0xff0000, 'orange': 0xff8000, 'yellow': 0xffff00, 'green': 0x00ff00, 'blue' : 0x00bfff, 'purple' : 0x8000ff, 'pink': 0xff00ff}

def setLED(value):
    pycom.rgbled(LEDColors.color[value])
