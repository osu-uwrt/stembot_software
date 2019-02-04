import signal
import socket
import select
from time import sleep

# SIGINT Handler

def shutdown(signal, frame):

	sleep(1)
	print('Stopping UDP...')
	s.close()
	print('Exiting...')
	exit(0)
signal.signal(signal.SIGINT, shutdown)

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

def print_voltage(value):
	value=int(value.split("\n")[-2])
	percent=(value*12.1/867-11.1)/1.5
	percent=str(round(percent*100,2))
	print("Battery: " + percent+"%")



controller = open('/dev/input/js0','r')
print('Connecting to STEMbot...')
stembotConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stembotConn.connect(('192.168.1.112', 50000))
print('Connected!')

packet = []
heave = 0
surge = 0
turn = 0

while 1:
	readable, writable, exceptional = select.select([stembotConn, controller], [], [], 0)
	
	for a in readable:
		if a == stembotConn: # If stembot activity
			data = stembotConn.recv(1024)
			print_voltage(data.encode())

		if a == controller: # If controller data
			packet += [int(str(hex(ord(controller.read(1)))), 16)]
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
				set_thrusters((surge - turn) *25, (surge + turn) * 25, heave*25, heave * 25)
