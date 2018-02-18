import signal
import socket
import math
import RPi.GPIO as GPIO
from time import sleep

# SIGINT Handler

def shutdown(signal, frame):

    print '\n   Stopping UDP...'
    sock.close()

    print '   Stopping PWM...'
    portsurge.stop()
    stbdsurge.stop()
    portheave.stop() #changed vert to portheave
    stbdheave.stop() # added

    print '   Cleaning up...'
    GPIO.cleanup(PORTSURGE)
    GPIO.cleanup(STBDSURGE)
    GPIO.cleanup(PORTHEAVE) # changed from VERT to PORTHEAVE
    GPIO.cleanup(STBDHEAVE) # added

    print '   Exiting...'
    exit(0)

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
GPIO.setup(STBDSURGE, GPIO.OUT)
GPIO.setup(PORTHEAVE, GPIO.OUT) # changed VERT to PORTHEAVE
GPIO.setup(STBDHEAVE, GPIO.OUT) # added


print '   Setting PWM frequency...'
portsurge = GPIO.PWM(PORTSURGE, FREQ)
stbdsurge = GPIO.PWM(STBDSURGE, FREQ)
portheave = GPIO.PWM(PORTHEAVE, FREQ) # changed vert to portheave and VERT to PORTHEAVE
stbdheave = GPIO.PWM(STBDHEAVE, FREQ) # added

print '   Setting PWM duty cycle...'
portsurge.start(ZERO)
stbdsurge.start(ZERO)
portheave.start(ZERO) # changed vert to portheave
stbdheave.start(ZERO) # added
sleep(5) # needed for proper esc initialization

# The Loop

print '   Running...'
while 1:

    # Blocking Receive

    # Looking for ps3 input: if we have one, great. If not don't do anything
    try:
        data = sock.recv(2)
    except socket.error as (code, msg):
        pass

    # Update Current Trust Vector (based on input)

    if data[0] == 'x':
        x = ord(data[1]) - 127
    elif data[0] == 'y':
        y = ord(data[1]) - 127
    elif data[0] == 'z':
        z = ord(data[1]) - 127
    else:
        print '!?!?!?'
        print data
        print '!?!?!?'

    # Circularize and Rotate

    #Calculates the PWM for easch thruster

    #calculates based on input from ps3 controller
    r = math.hypot(x, y)
    r = r if r < 127 else 127
    t = math.atan2(y, x)
    t -= math.pi / 4
    p = r * math.sin(t)
    s = r * math.cos(t)

    # Transforms PWM value (us) to Duty Cycle
    p = dc(p + ZERO)
    s = dc(s + ZERO)
    ph = dc(z/2 + ZERO) # changed v to ph (for port heave) (also divided z by 2 to account for double heave thrusters)
    sh = dc(z/2 + ZERO) # added (named sh for starboard heave) (also divided z by 2 to account for double heave thrusters)

    # Write the new PWM to "Thrusters"

    portsurge.ChangeDutyCycle(p)
    stbdsurge.ChangeDutyCycle(s)
    portheave.ChangeDutyCycle(ph) # changed vert to portheave and v to ph
    stbdheave.ChangeDutyCycle(sh) # added

    # Did it Crash?
    print '   p: %5.2f  |  s: %5.2f  |  ph: %5.2f  |  sh: %5.2f' % (p, s, ph, sh) # changed v to ph and added sh

    # What I did:
    # Anywhere there was port, I changed it to portsurge
    # Anywhere there was stbd, I changed it to stbdsurge
    # Anywhere there was PORT, I changed it to PORTSURGE
    # Anywhere there was STBD, I changed it to STBDSURGE
    # Added comments throughout code to show non uniform changes (so we can check my work easier)
