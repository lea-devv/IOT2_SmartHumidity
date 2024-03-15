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

while True:
    if debounce(pb1) == 0: # Button pb1 is pressed
        move_motor(500, 'forward') # Open the motor
    if debounce(pb2) == 0: # Button pb2 is pressed
        move_motor(500, 'backward') # Close the motor
