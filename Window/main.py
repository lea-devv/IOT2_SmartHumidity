from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
IN1 = Pin(21, Pin.OUT)
IN2 = Pin(22, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

# Assuming a 4-wire stepper motor, we define sequences for 1 step
# For a 2-wire stepper motor, you would only need 2 sequences
sequence_forward = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence_backward = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

pb1 = Pin(4, Pin.IN, Pin.PULL_UP)
pb2 = Pin(0, Pin.IN, Pin.PULL_UP)

DEBOUNCE_DELAY = 50 # milliseconds

CLIENT_NAME = 'esp32_client' 
BROKER_ADDR = '4.231.174.166' 
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=5)

def states():
    window_closed = True

def debounce(pin):
    """Debounce a pin."""
    initial_value = pin.value()
    sleep(DEBOUNCE_DELAY / 1000.0) # Convert milliseconds to seconds
    return pin.value() == initial_value

def move_motor(steps, direction):
    """Move the motor a certain number of steps in a given direction."""
    sequence = sequence_forward if direction == 'forward' else sequence_backward
    for _ in range(steps):
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def sub_topic(topic, msg):
 print((topic, msg))
 if topic == b'window_command' and msg == b'received':
     print('ESP received "" message')
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
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()
    if msg = b'open' and window_closed = True:
        move_motor(500, 'forward')
        States.window_closed = False
        