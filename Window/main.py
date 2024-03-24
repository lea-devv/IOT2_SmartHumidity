from umqtt.simple import MQTTClient
from machine import Pin, Timer
from time import sleep
import ubinascii
import machine
import micropython

####################################################
#Initialize variables
client_name = ubinascii.hexlify(machine.unique_id())
broker_address = '4.231.174.166' 
mqttc = MQTTClient(client_name, broker_address)

autoclose_variable = b"autoclose_variable"
window_command = b"window_command"
pir_state = b"pir_state"

####################################################
IN1 = Pin(21, Pin.OUT)
IN2 = Pin(22, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence_forward = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence_backward = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
####################################################
button_open = Pin(0, Pin.IN)
button_close = Pin(15, Pin.IN)

####################################################
manual_window_timer = Timer(1)
timer_m = 5
timer_ms = 6000

####################################################
window_closed = True
manual_override = False
person = False
####################################################
def move_motor(steps, direction):
    #Moves the motor
    sequence = sequence_forward if direction == 'forward' else sequence_backward
    for _ in range(steps):
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def timeout_close(manual_window_timer):
    global manual_override
    move_motor(500, 'backward')
    window_closed = True
    manual_override = False
    
###################################################

def sub_topic(topic, msg):
    global window_closed
    global manual_override
    global timer_m, timer_ms
    global person
    
    try:
        decoded_msg = msg.decode('utf-8')
        decoded_topic = topic.decode('utf-8')
        if manual_override == False:
            if topic == window_command:
                str_window_closed = str(window_closed)
                str_person = str(person)
                if decoded_msg == "open":
                    if str_window_closed == "True" and str_person == "False":
                        move_motor(500, 'forward')
                        window_closed = False
                elif decoded_msg == "close":
                    if str_window_closed == "False":
                        move_motor(500, 'backward')
                        window_closed = True
            
        if topic == autoclose_variable:   
            timer_m = int(decoded_msg) 
            timer_ms = timer_m * 6000
                        
        if topic == pir_state:  
            person = str(decoded_msg)
            
    except Exception as e:
        print(f"Error processing MQTT message: {e}") 

####################################################
def connect_and_subscribe():
    try:
        mqttc.set_callback(sub_topic)
        mqttc.connect()
        print('Connected to MQTT broker')
        mqttc.subscribe(autoclose_variable)
        mqttc.subscribe(window_command)
        mqttc.subscribe(pir_state)

    except Exception as e:
        print('Failed to connect to MQTT broker:', e)

####################################################
#Run the code
connect_and_subscribe()

while True:
    mqttc.check_msg()
    bod1 = button_open.value() #button open debounce
    bcd1 = button_close.value() #button close debounce
    sleep(0.1)
    bod2 = button_open.value()
    bcd2 = button_close.value()
    if bod1 == 1 and bod2 == 0:
        move_motor(500, 'forward')
        window_closed = False
        manual_override = True
        manual_window_timer.init(period=timer_ms, mode=Timer.ONE_SHOT, callback=timeout_close)
    
    elif bcd1 == 1 and bcd2 == 0 and window_closed == False:
        window_closed = True
        move_motor(500, 'backward')
        
