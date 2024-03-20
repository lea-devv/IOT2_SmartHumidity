from machine import Pin, Timer
from time import sleep
from umqtt.simple import MQTTClient

CLIENT_NAME = 'esp32_client' # Choose a unique client name
BROKER_ADDR = '4.231.174.166' # Replace with your broker's address
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=5)

IN1 = Pin(21, Pin.OUT)
IN2 = Pin(22, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence_forward = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence_backward = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

pb1 = Pin(4, Pin.IN, Pin.PULL_UP)
pb2 = Pin(0, Pin.IN, Pin.PULL_UP)

DEBOUNCE_DELAY = 50 # milliseconds

def on_message_print(client, userdata, message):
    print("Received message:", int(message.payload))
    return message.payload

mqttc.set_callback(on_message_print)
def connect_and_subscribe():
    try:
        mqttc.connect()
        print('Connected to MQTT broker')
        # Subscribe to a topic (optional)
        mqttc.subscribe(b'window_command')
    except Exception as e:
        print('Failed to connect to MQTT broker:', e)

connect_and_subscribe()
class MotorController:
    def __init__():
        window_open = False
        window_open_timer = Timer(1)

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

    def timeout_close(timer):
        move_motor(500, 'backward')
        window_open = False

    def run():
        while True:
            if debounce(pb1) == 0: # Button pb1 is pressed
                move_motor(500, 'forward')# Open the motor
                window_open = True
                window_open_timer.init(period=10000, mode=Timer.ONE_SHOT, callback=self.timeout_close)
            
            if debounce(pb2) == 0: # Button pb2 is pressed
                move_motor(500, 'backward')
                window_open = False


MotorController.run()

