from machine import Pin, I2C
from bme680 import BME680_I2C

i2c = I2C(scl=Pin(22), sda=Pin(21))

bme = BME680_I2C(i2c=i2c)

gas = bme.gas
temperature = bme.temperature
humidity = bme.humidity

