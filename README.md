# pi-gui-lite
Have you ever wanted to use your Raspberry Pi without wiring up a hefty keyboard mouse and monitor setup or sshing into it?
PI-GUI-LITE is here to make your life easier!
Since these are the early days of this project, there is very very limited functionality right now, but expect it to grow into a much more functional tool as the days go by.

# What can it do?
Currently, the hardware hat is on version 1.0, with a few unfortunate mechanical mishaps but still operational with some hardware hacks.
![Image of stacking board in action](/images/titledemo.JPG)
## Hardware 
It comes with a 2.42 inch OLED SSD1309 display, 5 configurable MX switches and 3 general purpose LEDs. 10 stars on this repo and I will guarantee the development of Hat2.0.
Changes to be made:
- Mechanical resizing to not overlap with USB ports 
- Normal stacking header instead of extra tall one
- GPIO Pin breakout -> Will consider implementing either I2C or SPI or Both
- Possible GPIO expander
- Peripheral changes -> Number of switches? Rotary encoder? Different display?

## Software 
On the software side, there is currently a main python script (titlescript.py) to run as a mini OS, allowing you to browse through and run any 'installed' or connected python scripts. 
Current applications:
- Git Manager (Highly Recommended): Allows cloning git repos from a specified username in the .json and pulling currently installed git repos
- Example hardware apps: A red toggleable LED and 2 blinking alternating LEDs

Next Ideas:
- File Manager: Browse and manage files with ls, cd, cat, mv, rm
- Quality of Life bottom bar to show button functions

Dependencies include luma.oled, luma.core and gpiozero, although I will take feedback on whether to switch to RPI.gpIO.
