from umqtt.simple import MQTTClient
import network

ssid = 'KEA_Starlink'
password = 'KeaStarlink2023'
mqtt_server = '4.231.174.166'

topic_sub1 = b'window_command'
topic_sub2 = b'autoclose_variable'
topic_sub3 = b'pir_state'
topic_pub = b'hello'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
print('Connection successful')
print(station.ifconfig())