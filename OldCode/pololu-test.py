import maestro
from time import sleep
servo = maestro.Controller("/dev/ttyACM0")

servo.setAccel(0,0)      #set servo 0 acceleration to 0 (unrestrained)
servo.setTarget(0,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(1,0)      #set servo 1 acceleration to 0 (unrestrained)
servo.setTarget(1,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(2,0)      #set servo 2 acceleration to 0 (unrestrained)
servo.setTarget(2,6000)  #set servo to move to center position
sleep(2)
servo.setAccel(3,0)      #set servo 3 acceleration to 0 (unrestrained)
servo.setTarget(3,6000)  #set servo to move to center position

sleep(5)

servo.setTarget(0, 6200)
servo.setTarget(1, 6200)
servo.setTarget(2, 6200)
servo.setTarget(3, 6200)

sleep(3)

servo.setTarget(0, 6000)
servo.setTarget(1, 6000)
servo.setTarget(2, 6000)
servo.setTarget(3, 6000)


servo.close()
