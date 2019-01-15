import signal
import socket
import maestro
from time import sleep

PORTSURGE = 0
STBDSURGE = 1
FWDHEAVE = 2
AFTHEAVE = 3

def shutdown(signal, frame):

	stop_thrusters()
	print('Stopping UDP...')
	s.close()
	conn.close()
	print('Stopping Pololu...')
	servo.close()
	print('Exiting...')
	exit(0)

def wait_for_connect():

	print('Waiting for connection...')
	global conn
	conn, addr = s.accept()
	print('Connected to: ')
	print(addr)

def stop_thrusters():

	print('Stopping thrusters')
	# Allow all accelerations and stop thrusters (4000 full back, 8000 full forward)
	servo.setAccel(PORTSURGE,0)
	servo.setTarget(PORTSURGE,6000)
	servo.setAccel(STBDSURGE,0)  
	servo.setTarget(STBDSURGE,6000)
	servo.setAccel(FWDHEAVE,0)
	servo.setTarget(FWDHEAVE,6000)
	servo.setAccel(AFTHEAVE,0)
	servo.setTarget(AFTHEAVE,6000)


signal.signal(signal.SIGINT, shutdown)

print('Waiting for startup')
sleep(30)
print('Setting UDP mode...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False

while not connected:
	try:
		s.bind(('192.168.1.112', 50000))
		connected = True
	except:
		sleep(1)

s.listen(1);

print('Connecting to maestro...')

connected = False
while not connected:
	try:
		servo = maestro.Controller("/dev/ttyACM0")
		connected = True
	except:
		sleep(1)



stop_thrusters()
print('Waiting for thrusters to initialize...')
sleep(5)

print('STEMbot is online')

wait_for_connect()

while 1:

	try:
		data = conn.recv(8)
		conn.send('0')
	except:
		stop_thrusters()
		wait_for_connect()
		continue

	if not data:
		continue

	servo.setTarget(PORTSURGE, ord(data[0]) * 256 + ord(data[1]))
	servo.setTarget(STBDSURGE, ord(data[2]) * 256 + ord(data[3]))
	servo.setTarget(FWDHEAVE, ord(data[4]) * 256 + ord(data[5]))
	servo.setTarget(AFTHEAVE, ord(data[6]) * 256 + ord(data[7]))
	
