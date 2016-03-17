import signal
import socket

# SIGINT Handler

def shutdown(signal, frame):

    print '\n   Stopping UDP...'
    sock.close()

    print '   Stopping PS3...'
    controller.close()

    print '   Exiting...'
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# Joystick "Register" Mapper

def rectify_axis(byte):
    byte = 127 - byte
    if byte < 0:
        byte += 255
    return byte

# UDP Constants

ADDR = ('192.168.1.4', 1337)

# PS3 Read Buffer

packet = []

# UDP Setup

print '   Setting UDP mode...'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print '   Setting UDP buffers...'
right_x = ['x', 0]
right_y = ['y', 0]
left_y = ['z', 0]

# PS3 Setup

print '   Setting PS3 interface...'
controller = open('/dev/input/js0','r')

# The Loop

print '   Running...'
while 1:

    # Blocking Receive

    packet += [int(str(hex(ord(controller.read(1)))), 16)]

    # Process Packet

    if len(packet) == 8:

        # Is it a Stick?

        if packet[6] == 2:

            # Right Stick X Update

            if packet[7] == 2:
                right_x[1] = rectify_axis(packet[5])
                sock.sendto('%c%c' % (right_x[0], right_x[1]), ADDR)
                print '   x: %3i' % right_x[1]

            # Right Stick Y Update

            elif packet[7] == 3:
                right_y[1] = rectify_axis(packet[5])
                sock.sendto('%c%c' % (right_y[0], right_y[1]), ADDR)
                print '   y: %3i' % right_y[1]

            # Left Stick Y Update

            elif packet[7] == 1:
                left_y[1] = rectify_axis(packet[5])
                sock.sendto('%c%c' % (left_y[0], left_y[1]), ADDR)
                print '   z: %3i' % left_y[1]

        # Reset Packet Buffer

        packet = []
