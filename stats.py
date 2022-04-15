# Created by: Sandeep Gaikwad
# Stats script for 128x64 SPI OLED Display For Raspberry Pi 4
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://github.com/sandeep-mg/SPI-OLED-Display

import time
import board
import digitalio
import subprocess
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 32 if needed
BORDER = 5

# Use for I2C. (BETA)
#i2c = board.I2C()
#oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Use for SPI
spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D5)
oled_dc = digitalio.DigitalInOut(board.D6)
oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.

padding = -2
top = padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('PixelOperator.ttf', 16)

while True:

    draw.rectangle((0,0,oled.width,oled.height), outline=0, fill=0)
    
	# Draw Some Text
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    cmd = "top -bn1 | grep load | awk '{printf \"CPU:%.2f%%  \", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )

    #cmd = "free -m | awk 'NR==2{printf \"Mem:%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    cmd = "free -m | awk 'NR==2{printf \"Mem:%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )

    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True)
    
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.  
    draw.text((x,top+2),"IP: "+str(IP,'utf-8'),font=font,fill=255,)
    draw.text((x,top+18),str(CPU,'utf-8')+" "+str(temp,'utf-8'),font=font,fill=255,)
    draw.text((x,top+34),str(MemUsage,'utf-8'),font=font,fill=255,)
    draw.text((x,top+50),str(Disk,'utf-8'),font=font,fill=255,)


    # Display image
    oled.image(image)
    oled.show()
    time.sleep(.1)
