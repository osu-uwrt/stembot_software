import maestro
from time import sleep
servo = maestro.Controller()
servo.setAccel(0,0)      #set servo 0 acceleration to 0 (unrestrained)
servo.setTarget(0,6000)  #set servo to move to center position
while True:
	sleep(5)
servo.close
