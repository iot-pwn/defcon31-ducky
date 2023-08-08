
# Switch 1 - Position 1 - GPIO9
# Switch 1 - Position 2 - GPIO10
# Switch 2 - Position 1 - GPIO11
# Switch 2 - Position 2 - GPIO12
# Switch 3 - Position 1 - GPIO0
# Switch 3 - Position 2 - GPIO1
# Switch 3 - Position 3 - GPIO2
# Switch 3 - Position 4 - GPIO3
# Button 1 - GPIO4
# Button 2 - GPIO5
# Neopixel - GPIO6
# Buzzer - GPIO7

import asyncio

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

NOTE_C = 262  # C4
NOTE_D = 294  # D4
NOTE_E = 330  # E4
NOTE_F = 349  # F4
NOTE_G = 392  # G4
NOTE_A = 440  # A4
NOTE_B = 494  # B4

NOTE_C6 = 1046
NOTE_D6 = 1174
NOTE_E6 = 1318
NOTE_F6 = 1396
NOTE_G6 = 1567
NOTE_A6 = 1760
NOTE_B6 = 1975

enableRandomBeep = False
# setup buzzer on GP18

enableSirenMode = False

blinkeyState = 0
inBlinkeyMode = False

inMenu = False

menuStarted = False

def setNeoPixelColor(pixel, color):
    pixel.fill(color)
    pixel.show()

def startBlinkeyMode(pixel):
    global blinkeyState
    setNeoPixelColor(pixel, BLUE)
    blinkeyState = 1

def updateBlinkeyMode(pixel):
    global blinkeyState
    if(blinkeyState == 1):
        setNeoPixelColor(pixel, PURPLE)
    elif(blinkeyState == 2):
        setNeoPixelColor(pixel, RED)
    elif(blinkeyState == 3):
        setNeoPixelColor(pixel, CYAN)
    elif(blinkeyState == 4):
        setNeoPixelColor(pixel, YELLOW)
    elif(blinkeyState == 5):
        setNeoPixelColor(pixel, GREEN)
    elif(blinkeyState == 0):
        setNeoPixelColor(pixel, BLUE)

    blinkeyState += 1
    blinkeyState = blinkeyState % 6

def playBuzzer(freq, duration):
    # freequency in Hz
    # duration in msec
    playTime = duration / 1000
    print("Playing ", freq, " for ", duration, "msec", playTime, "sec")

    simpleio.tone(board.GP7,freq,duration=playTime)


def enterMenu():
    global inMenu, pixel
    print("Entering menu")
    playBuzzer(NOTE_B,100)
    setNeoPixelColor(pixel, RED)
    inMenu = True

def exitMenu():
    global inMenu, enableSirenMode, pixel
    print("Leaving Menu")
    playBuzzer(NOTE_C,100)
    setNeoPixelColor(pixel, GREEN)
    inMenu = False
    enableSirenMode = False

async def blink_neo_pixel(pixel):
    global inBlinkeyMode
    print("starting blink_neo_pixel")
    while True:
        if(inBlinkeyMode == True):
            updateBlinkeyMode(pixel)
        await asyncio.sleep(0.1)

async def randomBeepTask():
    global enableRandomBeep
    beepTimer = 5
    firstTime = True
    while True:
        if(enableRandomBeep):
            if(firstTime):
                await asyncio.sleep(beepTimer)
                firstTime = False
            playBuzzer(NOTE_D, 100)
            beepTimer = random.randrange(5,30)
        await asyncio.sleep(beepTimer)

async def sirenTask():
    global enableSirenMode,pixel
    sounds = [NOTE_C6,
    NOTE_D6,
    NOTE_E6,
    NOTE_F6,
    NOTE_G6,
    NOTE_A6,
    NOTE_B6
    ]
    up = True
    blue = True
    while True:
        if(enableSirenMode):
            print("Starting Siren")
            for i in range(0,7):
                if(blue):
                    setNeoPixelColor(pixel, BLUE)
                else:
                    setNeoPixelColor(pixel, RED)
                blue = not blue
                if(up):
                    playBuzzer(sounds[i],100)
                else:
                    playBuzzer(sounds[6-i],100)
                await asyncio.sleep(0.05)
            up = not up
        await asyncio.sleep(0.01)


async def monitor_buttons(button1, button2):
    global inBlinkeyMode, inMenu, enableRandomBeep, enableSirenMode,pixel
    print("starting monitor_buttons")
    sawButton1 = False
    sawButton2 = False
    menuStarted = False
    menuExited = False
    menu_option = 0
    button1Down = False
    button2Down = False
    inColorSelectMode = False
    while True:
        button1.update()
        button2.update()

        button1Pushed = button1.fell
        button2Pushed = button2.fell
        button1Released = button1.rose
        button2Released = button2.rose
        button1Held = not button1.value
        button2Held = not button2.value

        if(button1Pushed):
            print("Button 1 pushed")
            button1Down = True
        if(button2Pushed):
            print("Button 2 pushed")
            button2Down = True
        if(button1Released):
            print("Button 1 released")
            if(button1Down):
                print("push and released")
            #button1Down = False
        if(button2Released):
            print("Button 2 released")
            if(button1Down):
                print("push and released")
            #button2Down = False



        if(inMenu == False):
            if(button1Down and button2Down):
                menuStarted = True
            if(button1Released):
                if(menuStarted == True):
                    enterMenu()
                    menuStarted = False
                    button1Down = False
                    button2Down = False
                elif(button1Down):
                    # Run selected payload
                    setNeoPixelColor(pixel,RED)
                    payload = selectPayload()
                    print("Running ", payload)
                    runScript(payload)
                    print("Done")
                    setNeoPixelColor(pixel,GREEN)
                button1Down = False

            if(button2Released):
                if(menuStarted == True):
                    enterMenu()
                    menuStarted = False
                    button1Down = False
                    button2Down = False
                elif(button2Down):
                    if(inBlinkeyMode == False):
                        print("start blinkey mode")
                        setNeoPixelColor(pixel,CYAN)
                        #playBuzzer(262,100)
                        inBlinkeyMode = True
                        startBlinkeyMode(pixel)
                    else:
                        print("Stopping Blinkey Mode")
                        setNeoPixelColor(pixel,GREEN)
                        inBlinkeyMode = False
                button2Down = False

        else:
            if(button1Down and button2Down):
                menuExited = True
            if(button1Released):
                if(menuExited):
                    exitMenu()
                    menuExited = False
                    button1Down = False
                    button2Down = False
                elif(button1Down):
                    if(inColorSelectMode):
                        #advance colors
                        updateBlinkeyMode(pixel)
                    else:
                        # Go to next menu option
                        menu_option += 1
                        menu_option = menu_option % 3
                        print("Current menu option", menu_option)
                button1Down = False
            if(button2Released):
                if(menuExited):
                    exitMenu()
                    menuExited = False
                    button1Down = False
                    button2Down = False
                elif(button2Down):
                    if(inColorSelectMode):
                        inColorSelectMode = False
                    else:
                        # select curent menu option
                        if(menu_option == 0):
                            # color select
                            print("Select Color")
                            inColorSelectMode = True
                        elif(menu_option == 1):
                            # random beep
                            print("Random Beep")
                            enableRandomBeep = not enableRandomBeep
                        elif(menu_option == 2):
                            # siren mode
                            print("Siren mode")
                            enableSirenMode = True
                button2Down = False

        await asyncio.sleep(0)
