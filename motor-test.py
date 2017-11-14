import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)


s=GPIO.PWM(10, 50)
h=GPIO.PWM(12, 50)
v=GPIO.PWM(8, 50)
p=GPIO.PWM(16, 50)

s.start((1500*50)/10000)
p.start((1500*50)/10000)
v.start((1500*50)/10000)
h.start((1500*50)/10000)

sleep(8)

p.ChangeDutyCycle((1600*50)/10000)
s.ChangeDutyCycle((1600*50)/10000)
h.ChangeDutyCycle((1600*50)/10000)
v.ChangeDutyCycle((1600*50)/10000)

sleep(3)

p.stop()
s.stop()
h.stop()
v.stop()

GPIO.cleanup()
