import digitalio
from digitalio import DigitalInOut, Pull
import board
from board import *
from adafruit_debouncer import Debouncer

button1_pin = DigitalInOut(board.GP4) # defaults to input
button1_pin.pull = Pull.UP      # turn on internal pull-up resistor
button1 =  Debouncer(button1_pin)
button1.update()
button1Pushed = button1.rose

button2_pin = DigitalInOut(board.GP5) # defaults to input
button2_pin.pull = Pull.UP      # turn on internal pull-up resistor
button2 =  Debouncer(button2_pin)
button2.update()
button2Pushed = button2.rose

# payload1 = GPIO0 to GND
# payload2 = GPIO1 to GND
# payload3 = GPIO2 to GND
# payload4 = GPIO3 to GND
#init payload selection switch
payload1Pin = digitalio.DigitalInOut(GP0)
payload1Pin.switch_to_input(pull=digitalio.Pull.UP)
payload2Pin = digitalio.DigitalInOut(GP1)
payload2Pin.switch_to_input(pull=digitalio.Pull.UP)
payload3Pin = digitalio.DigitalInOut(GP2)
payload3Pin.switch_to_input(pull=digitalio.Pull.UP)
payload4Pin = digitalio.DigitalInOut(GP3)
payload4Pin.switch_to_input(pull=digitalio.Pull.UP)

# check GP9 for setup mode
progStatusPin = digitalio.DigitalInOut(GP9)
progStatusPin.switch_to_input(pull=digitalio.Pull.UP)

eyes_enable = DigitalInOut(board.GP8)
eyes_enable.direction = digitalio.Direction.OUTPUT
eyes_enable.value = True