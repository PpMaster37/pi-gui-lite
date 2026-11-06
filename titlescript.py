from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309

from time import sleep

from gpiozero import Button, LED

import blinkhello as blinkhello
import titlescreen as titlescreen
import christmaslights as clights

SCRIPT_LIBRARY = [titlescreen, blinkhello, clights]
SCRIPT_SELECT = 0

requested_script = None

b0 = Button(22, pull_up=None, active_state=False, bounce_time=0.05)
b1 = Button(23, pull_up=None, active_state=False, bounce_time=0.05)
b2 = Button(24, pull_up=None, active_state=False, bounce_time=0.05)
b3 = Button(25, pull_up=None, active_state=False, bounce_time=0.05)
b4 = Button(26, pull_up=None, active_state=False, bounce_time=0.05) 

BUTTON_ARRAY = [b0, b1, b2, b3, b4]

serial = i2c(port=1, address=0x3C)
device = ssd1309(serial, rotate=2, width=128, height=64)
serial.command(0xAF)

def main_loop():
    global SCRIPT_SELECT
    SCRIPT_SELECT = 0
    print("MAIN LOOP RUNNING")
    global requested_script
    requested_script = None
    while requested_script is None:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 20), SCRIPT_LIBRARY[SCRIPT_SELECT].file_text_data, fill="white")
        sleep(0.2)

def main_rebind():
    print("REBOUND")
    b4.when_pressed = cycleRight
    b0.when_pressed = cycleLeft
    b1.when_pressed = enterScript

def cycleRight():
    print("RIGHT PRESSED")
    global SCRIPT_SELECT
    if(SCRIPT_SELECT == len(SCRIPT_LIBRARY) - 1):
        SCRIPT_SELECT = 0
    else:
        SCRIPT_SELECT += 1

def cycleLeft():
    print("LEFT PRESSED")
    global SCRIPT_SELECT
    if(SCRIPT_SELECT == 0):
        SCRIPT_SELECT = len(SCRIPT_LIBRARY) - 1
    else:
        SCRIPT_SELECT -= 1

def enterScript():
    global requested_script
    requested_script = SCRIPT_SELECT

sleep(1)
while True:
    main_rebind()
    main_loop()

    if requested_script == 0:
        continue

    b0.when_pressed = None
    b1.when_pressed = None
    b2.when_pressed = None
    b3.when_pressed = None
    b4.when_pressed = None

    SCRIPT_LIBRARY[requested_script].run(device, BUTTON_ARRAY)