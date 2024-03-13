#https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/usage
from time import time, sleep

import Adafruit_SSD1306
import Adafruit_DHT

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from gpiozero import MotionSensor

pir = MotionSensor(4)

#################################################

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

disp.clear()
disp.display()

font = ImageFont.truetype('calibri-bold.ttf', 22)

##################################################

dht11 = Adafruit_DHT.DHT11
dht11_pin = 17

def read_dht11_data():
    humidity, temperature = Adafruit_DHT.read_retry(dht11, dht11_pin)
    if humidity is not None and temperature is not None:
        return humidity, temperature


##################################################

def draw_display():
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)

    humidity, temperature = read_dht11_data()

    humidity_formated = "Hum: " + str(humidity) + " %"
    temperature_formated = "Temp: " + str(temperature) + " °C"

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
    draw_display()
    sleep(1)
    
##################################################