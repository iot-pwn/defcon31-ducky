# License : GPLv2.0
# copyright (c) 2026  Dave Bailey, Aask
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support


import supervisor
import os
import pwmio
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


# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

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

# turn off automatically reloading when files are written to the pico
supervisor.runtime.autoreload = False

if(board.board_id == 'raspberry_pi_pico' or board.board_id == 'raspberry_pi_pico2'):
    led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
elif(board.board_id == 'raspberry_pi_pico_w' or board.board_id == 'raspberry_pi_pico2_w'):
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()

async def run_payload_on_startup():
    progStatus = False
    progStatus = getProgrammingStatus()
    print("progStatus", progStatus)
    if(progStatus == False):
        print("Finding payload")
        if "loot.bin" in os.listdir("/"):
            print("loot.bin exists, skipping payload execution.")
        else:
            payload = selectPayload()
            await asyncio.sleep(0.1)
            setNeoPixelColor(pixel,RED)
            print("Running")
            await runScript(payload)
    else:
        print("Done")


#ORDER = neopixel.GRB
#ORDER=(1,0,2,3)
setNeoPixelColor(pixel,GREEN)



# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

led_state = False



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
    button_task = asyncio.create_task(monitor_buttons())
    random_beep_task = asyncio.create_task(randomBeepTask())
    siren_task = asyncio.create_task(sirenTask())
    script_task = asyncio.create_task(run_payload_on_startup())
    print("Starting Wifi")
    startWiFi()
    print("Starting Web Service")
    webservice_task = asyncio.create_task(startWebService())
    await asyncio.gather(pico_led_task, neopixel_task,button_task,random_beep_task,siren_task,webservice_task,script_task)

asyncio.run(main_loop())
