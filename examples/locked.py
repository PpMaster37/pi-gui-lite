from gpiozero import LED

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
from datetime import timedelta

import time

file_text_data = "LOCK IN"

timer_val = 0
timer = False

def timer_edit(delta):
    global timer_val
    timer_val += delta

def toggle_timer():
    global timer
    timer = not timer

def run(device, BUTTON_ARRAY):
    global timer_val
    global timer
    print("Lock in time")
    exitButton = BUTTON_ARRAY[4]
    timerSmallUp = BUTTON_ARRAY[0]
    timerLargeUp = BUTTON_ARRAY[1]
    timerDown = BUTTON_ARRAY[2]
    timerToggle = BUTTON_ARRAY[3]
    red = LED(27)
    green = LED(18)
    timerSmallUp.when_pressed = lambda: timer_edit(300)
    timerLargeUp.when_pressed = lambda: timer_edit(1800)
    timerDown.when_pressed = lambda: timer_edit(-300)
    timerToggle.when_pressed = toggle_timer
    while not exitButton.is_pressed:
        if(timer):
            timer_val -= 1
            time.sleep(0.9999)
        with canvas(device) as draw:
            draw.text((50, 20), "LOCKED", fill="white")
            draw.text((40, 60), str(timedelta(seconds=timer_val)))
        
