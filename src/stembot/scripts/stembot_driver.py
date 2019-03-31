#!/usr/bin/env python

import rospy
import socket
import select
from time import sleep
from sensor_msgs.msg import Joy


stembotConn = None


def joyCB(event):
    surge = event.axes[4]
    turn = event.axes[3]
    heave = event.axes[1]

    if abs(turn) < .05:
        turn = 0
    if abs(surge) < .05:
        surge = 0
    if abs(heave) < .05:
        heave = 0
    packet = []
    ps = (surge - turn) * 25
    ss = (surge + turn) * 25 
    fh = heave * 25
    ah = heave * 25

    data = bytearray()
    data.append(int((6000 + 20 * -ps)/256))
    data.append(int((6000 + 20 * -ps)%256))
    data.append(int((6000 + 20 * -ss)/256))
    data.append(int((6000 + 20 * -ss)%256))
    data.append(int((6000 + 20 * fh)/256))
    data.append(int((6000 + 20 * fh)%256))
    data.append(int((6000 + 20 * -ah)/256))
    data.append(int((6000 + 20 * -ah)%256))
    stembotConn.sendall(data)

battery = 0

def print_voltage(value):
    global battery
    value=int(value.split("\n")[-2])
    percent=(value*12.35/910-11.1)/1.5
    if battery == 0:
        battery = percent
    battery = .999* battery + .001*percent
    percent=str(round(battery*100,2))
    print("Battery: " + percent+"%")

def main():
    global stembotConn

    rospy.init_node('stembot_driver')

    print('Connecting to STEMbot...')
    while not rospy.is_shutdown() and stembotConn == None :
        try:
            stembotConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            stembotConn.settimeout(1)
            stembotConn.connect(('192.168.1.112', 30000))
        except Exception as ex:
            print(ex)
            stembotConn = None
            sleep(1)
    print('Connected!')

    rospy.Subscriber('/joy', Joy, joyCB, queue_size=1)

    while not rospy.is_shutdown():
        readable, writable, exceptional = select.select([stembotConn], [], [], 0)
        
        for a in readable:
            if a == stembotConn: # If stembot activity
                data = stembotConn.recv(1024)
                print_voltage(data.encode())
        sleep(.01)

    stembotConn.close()


if __name__ == '__main__': main()