import signal
import socket
import subprocess
from time import sleep

# SIGINT Handler

def shutdown(signal, frame):

	print('Stopping thrusters...')
	set_thrusters(0,0,0,0)
	sleep(1)
	print('Stopping UDP...')
	s.close()
	print('Exiting...')
	exit(0)

# Set thruster percentages
# About 6% is deadzone
def set_thrusters(ps, ss, fh, ah):

	data = bytearray()
	data.append(int((6000 + 20 * ps)/256))
	data.append(int((6000 + 20 * ps)%256))
	data.append(int((6000 + 20 * ss)/256))
	data.append(int((6000 + 20 * ss)%256))
	data.append(int((6000 + 20 * fh)/256))
	data.append(int((6000 + 20 * fh)%256))
	data.append(int((6000 + 20 * ah)/256))
	data.append(int((6000 + 20 * ah)%256))
	s.sendall(data)

signal.signal(signal.SIGINT, shutdown)

print('Connecting to STEMbot...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.112', 50000))
print('Connected!')

while 1:
	speed = float(input("Speed: "))
	set_thrusters(speed, speed, speed, speed)
               
