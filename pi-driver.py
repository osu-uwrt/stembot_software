import signal
import socket
import math
import RPi.GPIO as GPIO

# SIGINT Handler

def shutdown(signal, frame):

    print '\n   Stopping UDP...'
    sock.close()

    print '   Stopping PWM...'
    port.stop()
    stbd.stop()
    vert.stop()

    print '   Cleaning up...'
    GPIO.cleanup(PORT)
    GPIO.cleanup(STBD)
    GPIO.cleanup(VERT)

    print '   Exiting...'
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# UDP Constants

ADDR = ('192.168.1.45', 1337)

# PWM Constants

ZERO = 7.5
FREQ = 50
PORT = 18
STBD = 16
VERT = 12

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
GPIO.setmode(GPIO.BOARD)

print '   Setting GPIO pins...'
GPIO.setup(PORT, GPIO.OUT)
GPIO.setup(STBD, GPIO.OUT)
GPIO.setup(VERT, GPIO.OUT)

print '   Setting PWM frequency...'
port = GPIO.PWM(PORT, FREQ)
stbd = GPIO.PWM(STBD, FREQ)
vert = GPIO.PWM(VERT, FREQ)

print '   Setting PWM duty cycle...'
port.start(ZERO)
stbd.start(ZERO)
vert.start(ZERO)

# The Loop

print '   Running...'
while 1:

    # Blocking Receive

    try:
        data = sock.recv(2)
    except socket.error as (code, msg):
        pass

    # Update Vector

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

    r = math.hypot(x, y)
    r = r if r < 127 else 127
    t = math.atan2(y, x)
    t -= math.pi / 4
    p = r * math.sin(t)
    s = r * math.cos(t)

    # Transform to Duty Cycle

    p = .02 * p + ZERO
    s = .02 * s + ZERO
    v = .02 * z + ZERO

    # Write to "Thrusters"

    port.ChangeDutyCycle(p)
    stbd.ChangeDutyCycle(s)
    vert.ChangeDutyCycle(v)

    # Did it Crash?

    print '   p: %5.2f  |  s: %5.2f  |  v: %5.2f' % (p, s, v)
