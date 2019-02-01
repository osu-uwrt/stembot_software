import signal
import socket
import maestro
import select
from time import sleep

PORTSURGE = 0
STBDSURGE = 1
FWDHEAVE = 2
AFTHEAVE = 3

def shutdown(signal, frame):

	stop_thrusters()
	print('Stopping sockets...')
	for s in conections:
		s.close()
	print('Stopping Pololu...')
	servo.close()
	print('Exiting...')
	exit(0)

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
	
def send_voltage(voltage):
	
	for s in conections:
		if s != incomingConnection:
			s.sendall(str(voltage).encode())

# Subscribe shutdown
signal.signal(signal.SIGINT, shutdown)

print('Setting up socket...')
incomingConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


connected = False
while not connected:
	try:
		incomingConnection.bind(('0.0.0.0', 50000))
		connected = True
	except:
		sleep(1)
incomingConnection.listen(1);
conections = [incomingConnection]


print('Connecting to maestro...')
connected = False
while not connected:
	try:
		servo = maestro.Controller("/dev/ttyACM0")
		connected = True
	except:
		sleep(1)


stop_thrusters()
print('STEMbot is online')

while 1:
	readable, writable, exceptional = select.select(conections, [], conections, 0)

	for s in readable:
		if s == incomingConnection:
			conn, addr = incomingConnection.accept()
			print("Connected to "+str(addr))
			conections.append(conn)
		else:
			try:
				data = s.recv(1024)
			except:
				conections.remove(s)
				stop_thrusters()
				print("Lost connection")
				continue
			if not data:
				conections.remove(s)
				stop_thrusters()
				print("Lost connection")
				continue
			servo.setTarget(PORTSURGE, ord(data[0]) * 256 + ord(data[1]))
			servo.setTarget(STBDSURGE, ord(data[2]) * 256 + ord(data[3]))
			servo.setTarget(FWDHEAVE, ord(data[4]) * 256 + ord(data[5]))
			servo.setTarget(AFTHEAVE, ord(data[6]) * 256 + ord(data[7]))
			
	#Read Voltage
	voltage = 0
	send_voltage(voltage)
	sleep(0.001)

	
	
