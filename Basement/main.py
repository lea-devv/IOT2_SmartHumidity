from umqtt.simple import MQTTClient
from time import sleep
import ubinascii
import machine
import micropython
from machine import Pin, I2C, Timer
from bme680 import BME680_I2C

####################################################
#Initialize variables
client_name = ubinascii.hexlify(machine.unique_id())
broker_address = '4.231.174.166' 
mqttc = MQTTClient(client_name, broker_address)

basement_gas = b"window_gas"
basement_hum = b"basement_hum"
basement_temp = b"basement_temp"
furnace_command = b"furnace_command"

####################################################
#Initialize sensor and pin
i2c = I2C(1, scl=Pin(22), sda=Pin(21))
bme = BME680_I2C(i2c=i2c)

furnace_led = Pin(26, Pin.OUT)
gas_led = Pin(4, Pin.OUT)
gas_timer = Timer(1)

####################################################
#Wait for BME680 to stabalize
sleep(10)
gas_led.value(0)

####################################################
def on_message_print(topic, message):
    print("Received message:", message)
    if message == b'on':
        furnace_led.value(1)
    elif message == b'off':
        furnace_led.value(0)

def connect_and_subscribe():
    try:
        mqttc.set_callback(on_message_print)
        mqttc.connect()
        print('Connected to MQTT broker')
        mqttc.subscribe(furnace_command)
    except Exception as e:
        print('Failed to connect to MQTT broker:', e)
  
def worse_air(gas_timer):
    print("Air quality is stable", bme.gas)
    gas_led.value(0)

####################################################
#Run the code
connect_and_subscribe()

while True:
    bme_first = bme.gas
    sleep(2)
    bme_second = bme.gas
    if bme_first - 2000 > bme_second:
        print (bme_first, bme_second)
        print("Warning: Air quality has worsened in the past 5 minuits")
        gas_led.value(1)
        gas_timer.init(period=60000, mode=Timer.ONE_SHOT, callback=worse_air)
    
    mqttc.publish(basement_gas, str(bme.gas))
    sleep(0.1)
    mqttc.publish(basement_temp, str(bme.temperature))
    sleep(0.1)
    mqttc.publish(basement_hum, str(bme.humidity))
    sleep(0.1)
    mqttc.check_msg()

