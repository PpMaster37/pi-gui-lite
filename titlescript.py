from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
from registry import load_registry, load_module

from time import sleep

from gpiozero import Button, LED

import examples.titlescreen as titlescreen

requested_script = None

registry = load_registry()
loaded_scripts = {}
loaded_scripts["title"] = titlescreen

for name, info in registry["modules"].items():
    if not info.get("enabled", True):
        print(f"skipping disabled: {name}")
        continue
    try:
        loaded_scripts[name] = load_module(name, info)
        print(f"Loaded: {name} from {info['path']}")
    except Exception as e:
        print(f"Failed to load {name}: {e}")

class AppCycler:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def keys(self):
        return list(self.data.keys())

    def current(self):
        keys = self.keys()
        if not keys:
            return None, None
        name = keys[self.index % len(keys)]
        return name, self.data[name]

    def next(self):
        keys = self.keys()
        if not keys:
            return None, None
        self.index = (self.index + 1) % len(keys)
        return self.current()

    def prev(self):
        keys = self.keys()
        if not keys:
            return None, None
        self.index = (self.index - 1) % len(keys)
        return self.current()

app_cycler = AppCycler(loaded_scripts)

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
    print("MAIN LOOP RUNNING")
    global requested_script
    requested_script = None
    while requested_script is None:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 20), app_cycler.current()[0], fill="white")
        sleep(0.2)

def main_rebind():
    print("REBOUND")
    b4.when_pressed = app_cycler.next
    b0.when_pressed = app_cycler.prev
    b1.when_pressed = enterScript
    b2.when_pressed = None
    b3.when_pressed = None

def enterScript():
    global requested_script
    requested_script = app_cycler.current()[1]

sleep(1)
while True:
    main_rebind()
    main_loop()

    if app_cycler.current()[0] == "title":
        continue

    b0.when_pressed = None
    b1.when_pressed = None
    b2.when_pressed = None
    b3.when_pressed = None
    b4.when_pressed = None

    requested_script.run(device, BUTTON_ARRAY)