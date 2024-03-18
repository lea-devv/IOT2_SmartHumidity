import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
ssid = 'KEA_Starlink'
password = 'KeaStarlink2023'
mqtt_server = '4.231.174.166'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub1 = b'window_command'
topic_sub2 = b'autoclose_variable'
topic_sub3 = b'pir_state'
topic_pub = b'hello'
last_message = 0
message_interval = 5
counter = 0
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
 pass
print('Connection successful')
print(station.ifconfig())