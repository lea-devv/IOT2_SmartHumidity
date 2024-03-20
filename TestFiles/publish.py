import paho.mqtt.publish as publish
import json
#import Adafruit_DHT
from time import sleep

humidity = 0
temperature = 0

#sensor = Adafruit_DHT.DHT11   #definer hvilken sensor du vil bruge
pin = 4  # Pin for Gpio på sensor
while True:
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)    #hvilke data der skal måles
    if humidity is not None and temperature is not None:   #kun send data når værdierne ikke er 0.
        payload = {"temperature" : temperature, "humidity" : humidity}    #definer pyloaden, det med rødt er det titlen på dataen, det med blåt er den data der faktisk bliver målt
        publish.single("furnace_command", "on" , hostname="4.231.174.166")  #Her kan bruges publish single og mulitple. Brug paho til bestemt topic, json sætter payload ind, bestem hvilkem host du vil publishe til via deres ip-adresse
        #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))  #ikke nødvændigt men godt tl at teste om det fungere
    else:
        print('Failed to get reading. Try again!')
    print("Sent")
    sleep(5)