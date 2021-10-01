#
# ZX Raspberry Keyboard Scanner v5
# @mrpjevans mrpjevans.com 2019
# MIT License (https://opensource.org/licenses/MIT) see LICENSE
#

import time, sys, os, uinput
from gpiozero import DigitalInputDevice, DigitalOutputDevice, PWMLED, LED

# KB1 (BCOM GPIO pins)
dataLines = [4,16,13,22,23,21]

# KB1 (BCOM GPIO pins)
addressLines = [5,6,20,24,26,12]

# The ZX Spectrum Keyboard Matrix (Mapped to modern keyboard)
keys = [
      ['Q', 'W', 'E', 'R', 'T','Y'],
      ['A', 'S', 'D', 'F', 'G','H'],
      ['Z', 'X', 'C', 'V', 'B','N'],
      ['P', 'BACKSPACE', 'U', 'I', 'O','M'],
      ['TAB', 'ENTER', 'J', 'K', 'L','SPACE'],
      ['DOT', 'RESERVED', 'LEFT', 'UP', 'DOWN','RIGHT']
]


# Function key mode
funcKeys = [
      ['1', '2', '3', '4', '5','6'],
      ['A', 'S', 'GRAVE', 'DOLLAR', 'G','KPPLUS'],
      ['Z', 'X', 'QUESTION', 'SLASH', 'APOSTROPHE','N'],
      ['0', 'EQUAL', '7', '8', '9','M'],
      ['BACKSLASH', 'ENTER', 'J', 'KPASTERISK', 'MINUS','SPACE'],
      ['COMMA', 'RESERVED', 'LEFTBRACE', 'UP', 'DOWN','RIGHTBRACE']
]

ShiftKeys = [
      ['Q', 'W', 'E', 'R', 'T','Y'],
      ['A', 'S', 'D', 'F', 'G','H'],
      ['Z', 'X', 'C', 'V', 'B','N'],
      ['P', 'DELETE', 'U', 'I', 'O','M'],
      ['ESC', 'ENTER', 'J', 'K', 'L','SEMICOLON'],
      ['SEMICOLON', 'RESERVED', 'LEFTBRACE', 'UP', 'DOWN','RIGHTBRACE']
]


# Track keypresses so we can support multiple keys
keyTrack = [
    [False, False, False, False, False, False],
    [False, False, False, False, False, False],
    [False, False, False, False, False, False],
    [False, False, False, False, False, False],
    [False, False, False, False, False, False],
    [False, False, False, False, False, False]
]



# Well this is annoying
device = uinput.Device([
        uinput.KEY_A, uinput.KEY_B, uinput.KEY_C, uinput.KEY_D, uinput.KEY_E, uinput.KEY_F, uinput.KEY_G, uinput.KEY_H,
        uinput.KEY_I, uinput.KEY_J, uinput.KEY_K, uinput.KEY_L, uinput.KEY_M, uinput.KEY_N, uinput.KEY_O, uinput.KEY_P,
        uinput.KEY_Q, uinput.KEY_R, uinput.KEY_S, uinput.KEY_T, uinput.KEY_U, uinput.KEY_V, uinput.KEY_W, uinput.KEY_X,
        uinput.KEY_Y, uinput.KEY_Z, uinput.KEY_0, uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4, uinput.KEY_5,
        uinput.KEY_6, uinput.KEY_7, uinput.KEY_8, uinput.KEY_9, uinput.KEY_TAB, uinput.KEY_MINUS, uinput.KEY_DOLLAR,
        uinput.KEY_LEFTSHIFT, uinput.KEY_ENTER, uinput.KEY_SPACE, uinput.KEY_LEFTCTRL, uinput.KEY_KPPLUS,
        uinput.KEY_DASHBOARD, uinput.KEY_QUESTION, uinput.KEY_LEFTBRACE, uinput.KEY_RIGHTBRACE, uinput.KEY_SLASH,
        uinput.KEY_BACKSLASH,uinput.KEY_EQUAL,uinput.KEY_APOSTROPHE,uinput.KEY_GRAVE,uinput.KEY_KPDOT,
        uinput.KEY_F10, uinput.KEY_F3, uinput.KEY_F4, uinput.KEY_F5, uinput.KEY_FN, uinput.KEY_SEMICOLON,
        uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT, uinput.KEY_RESERVED, uinput.KEY_DELETE, 
        uinput.KEY_ESC, uinput.KEY_BACKSPACE, uinput.KEY_COMMA, uinput.KEY_DOT, uinput.KEY_CAPSLOCK, uinput.KEY_KPASTERISK
        ])

# KB1 (BCOM GPIO pins)
dataLineIds = [4,16,13,22,23,21]
dataLines = [];

# KB2 (BCOM GPIO pins)
addressLineIds = [5,6,20,24,26,12]
addressLines = []


# Set all data lines to input
for dataLineId in dataLineIds:
    dataLines.append(DigitalInputDevice(dataLineId, True))

# Set all address lines for output
for addressLineId in addressLineIds:
    addressLines.append(DigitalOutputDevice(addressLineId, True, True))

# Keyboard mode and reset button
mode_led = PWMLED(17)
mode_handler = 0
#mode_led.pulse()

# 0 = Spectrum, 1 = Function Keys
keyboardMode = 0


# Announce
print("Running")

#led = LED(17)
#led.on()


try:

    # Loop forever
    while True:

        # Individually set each address line low
        for addressLine in range(6):

            # Set low
            addressLines[addressLine].off()

            # Scan data lines
            for dataLine in range(6):

                # Get state and details for this button
                isPressed = dataLines[dataLine].value == 1
                #print('isPressed ' + str(isPressed))
                if(keyboardMode == 0):
                    keyPressed = keys[addressLine][dataLine]
                elif(keyboardMode == 1):
                    keyPressed = funcKeys[addressLine][dataLine]
                elif(keyboardMode == 2):
                    keyPressed = ShiftKeys[addressLine][dataLine]

                keyCode = getattr(uinput, 'KEY_' + keyPressed)
                #print('keyCode ' + str(keyCode))
                # If pressed for the first time
                if(isPressed and keyTrack[addressLine][dataLine] == False):
 
                    # Press the key and make a note
                    #print('Pressing keyPressed' + keyPressed)
                    device.emit(keyCode, 1)
                    keyTrack[addressLine][dataLine] = True
                    
                    if(keyTrack[5][1] == True and keyPressed == 'RESERVED' and keyboardMode == 0):
                        keyboardMode = 1
                        mode_led.value = 1
                    elif(keyTrack[5][1] == True and keyPressed == 'RESERVED' and keyboardMode == 1):
                        keyboardMode = 2
                        mode_led.pulse()
                        device.emit(getattr(uinput, 'KEY_LEFTSHIFT'), 1)
                    elif(keyTrack[5][1] == True and keyPressed == 'RESERVED' and keyboardMode == 2):
                        keyboardMode = 0
                        device.emit(getattr(uinput, 'KEY_LEFTSHIFT'), 0)
                        mode_led.value = 0

                # If not pressed now but was pressed on last check
                elif(not isPressed and keyTrack[addressLine][dataLine] == True):

                    # Release the key and make a note
                    #print('Releasing ' + keyPressed)
                    device.emit(keyCode, 0)
                    keyTrack[addressLine][dataLine] = False

            # Set high
            addressLines[addressLine].on()
            

            
        # Allow the CPU to breathe
        time.sleep(0.01)


except KeyboardInterrupt:
    sys.exit(0)
