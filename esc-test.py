import signal
import socket
import math
import RPi.GPIO as GPIO
from time import sleep

#-------#
# SETUP #
#-------#
signal.signal(signal.SIGINT, shutdown)

# UDP Constants

ADDR = ('192.168.1.122', 1337)

# PWM Constants
def dc(pwm):
    if pwm > 1900:
        pwm = 1900
    if pwm < 1100:
        pwm = 1400

    return (pwm*50)/10000


ZERO = dc(1500) # number comes from neutral pwm converted to duty cycle
FREQ = 50

# Thruster PIN numbers (can be changed as long as they are then plugged into the right pin during set up)
# brown wire -> ground
# yellow/orange -> pi (PWM)
# red goes to nothing


PORTSURGE = 14 # white wire
STBDSURGE = 15 # grey
PORTHEAVE = 18 # purple
STBDHEAVE = 23 # green wire
# ground attached to blue
# PS3 Vector

x = 0
y = 0
z = 0

# UDP Setup

print '   Setting UDP mode...'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print '   Setting UDP bind...'
sock.bind(ADDR)

# PWM Setup
print '   Setting GPIO mode...'
GPIO.setmode(GPIO.BCM) #changed GPIO.BOARD to GPIO.BCM

print '   Setting GPIO pins...'
GPIO.setup(PORTSURGE, GPIO.OUT)

print '   Setting PWM frequency...'
portsurge = GPIO.PWM(PORTSURGE, FREQ)

print '   Setting PWM duty cycle...'
portsurge.start(ZERO)

sleep(5) # needed for proper esc initialization

# The Loop

print '   Running...'
while 1:
    sleep(5)
