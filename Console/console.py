#https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/usage
from time import time, sleep

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from gpiozero import MotionSensor

pir = MotionSensor(4)

#################################################

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

# Clear display.
disp.clear()
disp.display()

image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('calibri-bold.ttf', 22)

##################################################

humidity = 70
temperature = 30

humidity_formated = "Hum: " + str(humidity) + " %"
temperature_formated = "Temp: " + str(temperature) + " °C"

##################################################

draw.text((5, 5), humidity_formated, font=font, fill=255)
draw.text((5, 32), temperature_formated, font=font, fill=255)
disp.image(image)
disp.display()

##################################################
#Checks if there is a person in the room and changes the state accordingly
person_state = False

def motion():
    global person_state
    print("Motion has been detected")
    person_state = True

def no_motion():
    global person_state
    print("I'm all alone")
    person_state = False

pir.when_motion = motion
pir.when_no_motion = no_motion

##################################################

while True:
    sleep(1)
    
##################################################