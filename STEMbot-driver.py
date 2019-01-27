import signal
import socket
import subprocess
from time import sleep

# SIGINT Handler

def shutdown(signal, frame):

	sleep(1)
	print('Stopping UDP...')
	s.close()
	print('Exiting...')
	exit(0)

# Set thruster percentages
# About 6% is deadzone
def set_thrusters(ps, ss, fh, ah):

	data = bytearray()
	data.append(int((6000 + 20 * -ps)/256))
	data.append(int((6000 + 20 * -ps)%256))
	data.append(int((6000 + 20 * -ss)/256))
	data.append(int((6000 + 20 * -ss)%256))
	data.append(int((6000 + 20 * fh)/256))
	data.append(int((6000 + 20 * fh)%256))
	data.append(int((6000 + 20 * -ah)/256))
	data.append(int((6000 + 20 * -ah)%256))
	s.sendall(data)

def rectify_axis(byte):
    byte = 127 - byte
    if byte < 0:
        byte += 255
    return byte

signal.signal(signal.SIGINT, shutdown)

print('Connecting to STEMbot...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.112', 50000))
print('Connected!')

controller = open('/dev/input/js0','r')
packet = []

heave = 0
surge = 0
turn = 0

while 1:
	# Blocking Receive
	

	packet += [int(str(hex(ord(controller.read(1)))), 16)]


	# Process Packet

	if len(packet) == 8:


		# Is it a Stick?


		if packet[6] == 2:


			# Right Stick X Update

			if packet[7] == 3:
				turn = (rectify_axis(packet[5])-128)/128.0

			# Right Stick Y Update

			elif packet[7] == 4:
				surge = (rectify_axis(packet[5])-128)/128.0

			# Left Stick Y Update

			elif packet[7] == 1:
				heave = (rectify_axis(packet[5])-128)/128.0
		packet = []
		
		set_thrusters((surge - turn) *50, (surge + turn) * 50, heave*100, heave * 100)
	

               
