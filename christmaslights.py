from gpiozero import Button, LED

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309

import time

file_text_data = "CHRISTMAS LIGHTS"

def run(device, BUTTON_ARRAY):
    print("Christmas Lights Called")
    red = LED(27)
    red.on()
    green = LED(18)
    yellow = LED(17)
    exitButton = BUTTON_ARRAY[4]
    while not exitButton.is_pressed:
        with canvas(device) as draw:
            draw.text((10, 20), "MERRY CHRISTMAS", fill="white")
        red.toggle()
        green.toggle()
        time.sleep(1)