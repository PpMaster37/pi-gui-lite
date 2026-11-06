from gpiozero import Button, LED

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309

import time

file_text_data = "LED RED FILE"

def redToggle(red):
    print("RED LED TOGGLED")
    red.toggle()

def run(device, BUTTON_ARRAY):
    print("LED SCRIPT CALLED")
    redButton = BUTTON_ARRAY[3]
    exitButton = BUTTON_ARRAY[4]
    red = LED(27)
    redButton.when_pressed = lambda: redToggle(red)
    while not exitButton.is_pressed:
        with canvas(device) as draw:
            draw.text((10, 20), "PRESS FOR RED LED", fill="white")
        time.sleep(0.01)
