import signal
import socket
import math
import maestro
from time import sleep

# SIGINT Handler

def shutdown(signal, frame):

    print '\n   Stopping UDP...'
    sock.close()

    print '\n   Stopping Pololu...'
    servo.close()

    print '   Exiting...'
    exit(0)


def pwmHeave(input):
    if input < 14 and input > 0:
	pwm = 1500
    else:
	pwm = 800/130 * (input + 60) + 1100
    return pwm

def pwmSurge(input):
    if input < 14 and input > 0:
	pwm = 1500
    else:
	pwm = 800/255 * (input + 120) + 1100
    return pwm

#-------#
# SETUP #
#-------#
signal.signal(signal.SIGINT, shutdown)

# UDP Constants

ADDR = ('192.168.1.112', 1337) #stembot , port number

# PWM Constants
def dc(pwm):
    if pwm > 1900:
        pwm = 1900
    if pwm < 1100:
        pwm = 1400

    return (pwm*50)/10000


ZERO = dc(1500) # number comes from neutral pwm converted to duty cycle
FREQ = 50

# Set up pololu

servo = maestro.Controller("/dev/ttyACM0")

# Thruster PIN numbers (can be changed as long as they are then plugged into the right pin during set up)
# brown wire -> ground
# yellow/orange -> pi (PWM)
# red goes to nothing

# Declare Thruster Ports
PORTSURGE = 2 # white wire
STBDSURGE = 0 # grey
PORTHEAVE = 3 # purple
STBDHEAVE = 1 # green wire
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


print '   Thruster Initialization: Zero Thrust...'

servo.setAccel(PORTSURGE,0)      #set servo 0 acceleration to 0 (unrestrained)
servo.setTarget(PORTSURGE,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(STBDSURGE,0)      #set servo 1 acceleration to 0 (unrestrained)
servo.setTarget(STBDSURGE,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(PORTHEAVE,0)      #set servo 2 acceleration to 0 (unrestrained)
servo.setTarget(PORTHEAVE,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(STBDHEAVE,0)      #set servo 3 acceleration to 0 (unrestrained)
servo.setTarget(STBDHEAVE,6000)  #set servo to move to center position

sleep(5)

print '   Thruster Initialization Complete...'

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

    #Calculates the PWM for each thruster
    #Calculates based on input from ps3 controller

    r = math.hypot(x, y)
    r = r if r < 127 else 127
    t = math.atan2(y, x)
    t -= math.pi / 4
    p = r * math.sin(t) + ZERO
    s = r * math.cos(t) + ZERO
    ph = z/2 + ZERO
    sh = z/2 + ZERO

    # Write the new PWM to "Thrusters"

    servo.setTarget(PORTSURGE, 4 * int(pwmSurge(p)))

    servo.setTarget(STBDSURGE, 4 * int(pwmSurge(s)))

    servo.setTarget(PORTHEAVE, 4 * int(pwmHeave(ph)))

    servo.setTarget(STBDHEAVE, 4 * int(pwmHeave(sh)))


    # Did it Crash?
    print '   p: %5.2f  |  s: %5.2f  |  ph: %5.2f  |  sh: %5.2f' % (pwmSurge(p), pwmSurge(s), pwmHeave(ph), pwmHeave(sh)) # changed v to ph and added sh

    # What I did:
    # Anywhere there was port, I changed it to portsurge
    # Anywhere there was stbd, I changed it to stbdsurge
    # Anywhere there was PORT, I changed it to PORTSURGE
    # Anywhere there was STBD, I changed it to STBDSURGE
    # Added comments throughout code to show non uniform changes (so we can check my work easier)
