import signal
import socket
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
def set_thrusters(ps, ss, fh, ah):

	data = []
	data.extend(int(6000 + 20 * ps).to_bytes(2, byteorder='big'))
	data.extend(int(6000 + 20 * ss).to_bytes(2, byteorder='big'))
	data.extend(int(6000 + 20 * fh).to_bytes(2, byteorder='big'))
	data.extend(int(6000 + 20 * ah).to_bytes(2, byteorder='big'))
	s.sendall(data)

signal.signal(signal.SIGINT, shutdown)

print('Connecting to STEMbot...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.112', 50000))


while 1:
	set_thrusters(0.5, 0.5, 0.5, 0)
	sleep(0.5)
               
