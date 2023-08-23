# License : GPLv2.0
# copyright (c) 2022  Dave Bailey, Aask
# Author: Dave Bailey (dbisu, @daveisu)


import supervisor
import time
import digitalio
from digitalio import DigitalInOut, Pull
import board
from board import *
import pwmio
import neopixel
import random
import simpleio
from adafruit_debouncer import Debouncer
import asyncio
from duckyinpython import *
from badge import *
import wifi
from webapp import *




def startWiFi():
    import ipaddress
    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    print("Connect wifi")
    #wifi.radio.connect(secrets['ssid'],secrets['password'])
    wifi.radio.start_ap(secrets['ssid'],secrets['password'])

    HOST = repr(wifi.radio.ipv4_address_ap)
    PORT = 80        # Port to listen on
    print(HOST,PORT)


led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()


# turn off automatically reloading when files are written to the pico
supervisor.runtime.autoreload = False


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


#ORDER = neopixel.GRB
#ORDER=(1,0,2,3)
#pixel = neopixel.NeoPixel(board.GP6, 1, brightness=0.2, auto_write=False, pixel_order=ORDER)
setNeoPixelColor(pixel,GREEN)

eyes_enable = DigitalInOut(board.GP8)
eyes_enable.direction = digitalio.Direction.OUTPUT
eyes_enable.value = True

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

led_state = False


progStatus = False
progStatus = getProgrammingStatus()

if(progStatus == True):
    print("Update your payload")
else:
    # not in setup mode, inject the payload
    payload = selectPayload()
    print("Running ", payload)
    setNeoPixelColor(pixel,BLUE)
    runScript(payload)
    setNeoPixelColor(pixel,RED)
    print("Done")

enableRandomBeep = False
# setup buzzer on GP18

enableSirenMode = False

blinkeyState = 0
inBlinkeyMode = False

inMenu = False

menuStarted = False


#led_state = False

async def main_loop():
    global pico_led,pixel,button1,button2
    pico_led_task = asyncio.create_task(blink_pico_w_led(led))
    neopixel_task = asyncio.create_task(blink_neo_pixel(pixel))
    button_task = asyncio.create_task(monitor_buttons(button1,button2))
    random_beep_task = asyncio.create_task(randomBeepTask())
    siren_task = asyncio.create_task(sirenTask())
    print("Starting Wifi")
    startWiFi()
    print("Starting Web Service")
    webservice_task = asyncio.create_task(startWebService())
    await asyncio.gather(pico_led_task, neopixel_task,button_task,random_beep_task,siren_task,webservice_task)

asyncio.run(main_loop())
