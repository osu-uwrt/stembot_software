import RPi.GPIO as GPIO
from time import sleep


# pin setup
PORTSURGE = 8 # white wire
STBDSURGE = 10 # grey
PORTHEAVE = 12 # purple
STBDHEAVE = 16 # green wire

ZERO = 7.5 # number comes from neutral pwm converted to duty cycle
FREQ = 50

# PWM Setup
print '   Setting GPIO mode...'
GPIO.setmode(GPIO.BOARD)

print '   Setting GPIO pins...'
GPIO.setup(PORTSURGE, GPIO.OUT)
GPIO.setup(STBDSURGE, GPIO.OUT)
GPIO.setup(PORTHEAVE, GPIO.OUT)
GPIO.setup(STBDHEAVE, GPIO.OUT)


print '   Setting PWM frequency...'
portsurge = GPIO.PWM(PORTSURGE, FREQ)
stbdsurge = GPIO.PWM(STBDSURGE, FREQ)
portheave = GPIO.PWM(PORTHEAVE, FREQ)
stbdheave = GPIO.PWM(STBDHEAVE, FREQ)

print '   Setting PWM duty cycle...'
portsurge.start(ZERO)
stbdsurge.start(ZERO)
portheave.start(ZERO)
stbdheave.start(ZERO)
sleep(8)


# Start up the motors

pwm = 1600
dc = (FREQ * pwm) / 1000

print "Starting port surge"
portsurge.ChangeDutyCycle(dc)
sleep(3)
portsurge.stop()

print "Starting starboard surge"
stbdsurge.ChangeDutyCycle(dc)
sleep(3)
stbdsurge.stop()

print "Starting port heave"
portheave.ChangeDutyCycle(dc)
sleep(3)
portheave.stop()

print "Starting starboard heave"
stbdsurge.ChangeDutyCycle(dc)
sleep(3)
stbdheave.stop()

print "Test complete"

GPIO.cleanup()

print "GPIO cleaned up"
