import signal
import socket
import select
from time import sleep

import board
import busio
import adafruit_pca9685

PORTSURGE = 0
STBDSURGE = 1
FWDHEAVE = 2
AFTHEAVE = 3

def pulse_to_duty(pulse_us):
	return int(0xFFFF*(pulse_us/(1000000/hat.frequency)))

def shutdown(signal, frame):

	stop_thrusters()
	print('Stopping sockets...')
	for s in conections:
		s.close()
	print('Stopping Pololu...')
	hat.deinit()
	print('Exiting...')
	exit(0)

def stop_thrusters():
	
	print('Stopping thrusters')
	# Allow all accelerations and stop thrusters (4000 full back, 8000 full forward)
	neutral_signal = 1000
	hat.channels[PORTSURGE].duty_cycle = pulse_to_duty(neutral_signal)
	hat.channels[STBDSURGE].duty_cycle = pulse_to_duty(neutral_signal)
	hat.channels[FWDHEAVE].duty_cycle = pulse_to_duty(neutral_signal)
	hat.channels[AFTHEAVE].duty_cycle = pulse_to_duty(neutral_signal)
	
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
i2c = busio.I2C(board.SCL, board.SDA)
connected = False
while not connected:
	try:
		hat = adafruit_pca9685.PCA9685(i2c)
		connected = True
	except:
		sleep(1)

hat.frequency = 400

stop_thrusters()
print('STEMbot is online')

data = []

while 1:
	readable, writable, exceptional = select.select(conections, [], conections, 0)

	for s in readable:
		if s == incomingConnection:
			conn, addr = incomingConnection.accept()
			print("Connected to "+str(addr))
			conections.append(conn)
		else:
			try:
				data += s.recv(1024)
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

			while len(data) >= 8:
				hat.channels[PORTSURGE].duty_cycle = pulse_to_duty(data[0] * 256 + data[1])
				hat.channels[STBDSURGE].duty_cycle = pulse_to_duty(data[2] * 256 + data[3])
				hat.channels[FWDHEAVE].duty_cycle = pulse_to_duty(data[4] * 256 + data[5])
				hat.channels[AFTHEAVE].duty_cycle = pulse_to_duty(data[6] * 256 + data[7])
				data = data[8:]
			
	#Read Voltage
	#voltage = 0
	#send_voltage(voltage)
	#sleep(0.001)

	
	
