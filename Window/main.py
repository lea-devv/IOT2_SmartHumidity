from umqtt.simple import MQTTClient
from machine import Pin, Timer
from time import sleep
IN1 = Pin(21, Pin.OUT)
IN2 = Pin(22, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

manuel_window = Timer(1)
# Assuming a 4-wire stepper motor, we define sequences for 1 step
# For a 2-wire stepper motor, you would only need 2 sequences
sequence_forward = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence_backward = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

pb1 = Pin(4, Pin.IN)
pb2 = Pin(0, Pin.IN)

DEBOUNCE_DELAY = 50 # milliseconds

CLIENT_NAME = 'esp32_client' 
BROKER_ADDR = '4.231.174.166' 
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=5)

manual_window = Timer(1)
window_closed = True
integer= 5
def move_motor(steps, direction):
    """Move the motor a certain number of steps in a given direction."""
    sequence = sequence_forward if direction == 'forward' else sequence_backward
    for _ in range(steps):
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def timeout_close(manual_window):
        move_motor(500, 'backward')
        window_open = False
    

def sub_topic(topic, msg):
    global window_closed
    global timer_variable
    print((topic, msg))
    print(window_closed)
    if topic == b'window_command' and msg == b'open' and window_closed == True:
        move_motor(500, 'forward')
        window_closed = False
    if topic == b'window_command' and msg == b'close' and window_closed == False:
        move_motor(500, 'backward')
        window_closed = True
    if topic == b'autoclose_variable':
        integer = int(msg.decode('utf-8')) 
        print(integer)
        timer_variable = integer * 6000
        print(timer_variable)
      
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub1, topic_sub2, topic_sub3
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_topic)
    client.connect()
    client.subscribe(topic_sub1)
    client.subscribe(topic_sub2)
    client.subscribe(topic_sub3)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub1))
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub2))
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub3))
    return client
def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()
try:
     client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
    
while True:
    client.check_msg()
    first = pb2.value()
    sleep(0.01)
    second = pb2.value()
    fremad = pb1.value()
    sleep(0.01)
    fremad_slip = pb1.value()
    if fremad == 1 and fremad_slip == 0:
        move_motor(500, 'forward')
        print("Knap Trykkes")
        window_open = True
        global timer_variable
        manual_window.init(period= timer_variable, mode=Timer.ONE_SHOT, callback=timeout_close)
    elif first == 1 and second == 0:
        move_motor(500, 'backward')
        print("Knap sluppet")