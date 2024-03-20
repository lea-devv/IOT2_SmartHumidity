from machine import Pin, I2C
from bme680 import BME680_I2C
from umqtt.simple import MQTTClient
from time import sleep

#i2c = I2C(scl=Pin(22), sda=Pin(21))
#bme = BME680_I2C(i2c=i2c)
#gas = bme.gas
#temperature = bme.temperature
#humidity = bme.humidity

gas = 5
temperature = 20
humidity = 70

client_name = 'esp32_client' 
broker_ip = '4.231.174.166' 
mqttc = MQTTClient(client_name, broker_ip, keepalive=5)

def sub_topic(topic, msg):
    ...

def restart_and_reconnect():
    print("Failed to connect to MQTT Broker. Restarting")
    sleep(10)
    machine.reset()

while True:
    client.check_msg()