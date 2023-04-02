#!/usr/bin/env python3

import rclpy
import socket
import select
from time import sleep
from sensor_msgs.msg import Joy


stembotConn = None
thrustor_neutral = 1500
thrustor_min     = 800
thrustor_max     = 2200

def truncate(value, min, max):
    ret = value
    if ret < min:
        ret = min
    elif ret > max:
        ret = max
    
    return ret


def joyCB(event):
    #triggers are (trigger value + 1) / 2 because joy_node reports them as -1 to 1. we want them from 0 to 1
    heave_front = 1 - ((event.axes[5] + 1) / 2) # right trigger
    heave_aft = 1 - ((event.axes[2] + 1) / 2) # left trigger
    surge_port = event.axes[1] # left joystick
    surge_starboard = event.axes[4] # right joystick
        
    # ps = abs(max(thrustor_maximum * surge_port, 0))
    # ss = abs(max(thrustor_maximum * surge_starboard, 0))
    # fh = abs((heave_front - 1) / 2) * thrustor_maximum
    # ah = abs((heave_aft - 1) / 2) * thrustor_maximum
    
    thrustor_range = (thrustor_max - thrustor_min) / 2
    ps = (thrustor_range * surge_port) + thrustor_neutral
    ss = (thrustor_range * surge_starboard) + thrustor_neutral
    fh = (thrustor_range * heave_front) + thrustor_neutral
    ah = (thrustor_range * heave_aft) + thrustor_neutral
    
    ps = truncate(ps, thrustor_min, thrustor_max)
    ss = truncate(ss, thrustor_min, thrustor_max)
    fh = truncate(fh, thrustor_min, thrustor_max)
    ah = truncate(ah, thrustor_min, thrustor_max)
    
    print(ps)
    print(ss)
    print(fh)
    print(ah)
    print()
    
    # if abs(heave_front) < .05:
    #     heave_front = 0
    # if abs(heave_aft) < .05:
    #     heave_aft = 0
    # if abs(surge_port) < .05:
    #     surge_port = 0
    # if abs(surge_starboard) < .05:
    #     surge_starboard = 0

    data = bytearray()
    data.append(int(ps/256))
    data.append(int(ps%256))
    data.append(int(ss/256))
    data.append(int(ss%256))
    data.append(int(fh/256))
    data.append(int(fh%256))
    data.append(int(ah/256))
    data.append(int(ah%256))
    stembotConn.sendall(data)

battery = 0

def print_voltage(value):
    global battery
    value=int(value.split(b"\n")[-2])
    percent=(value*12.35/910-11.1)/1.5
    if battery == 0:
        battery = percent
    battery = .999* battery + .001*percent
    percent=str(round(battery*100,2))
    print("Battery: " + percent+"%")

def main():
    global stembotConn

    rclpy.init_node('stembot_driver')

    print('Connecting to STEMbot...')
    while rclpy.ok() and stembotConn == None :
        try:
            stembotConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            stembotConn.settimeout(1)
            address = rospy.get_param("~address")
            print("Connecting to:", address)
            stembotConn.connect((address, 50000))
        except Exception as ex:
            print(ex)
            stembotConn = None
            sleep(1)
    print('Connected!')
    print('Press Control+C to quit')

    rospy.Subscriber('/joy', Joy, joyCB, queue_size=1)

    while not rospy.is_shutdown():
        readable, writable, exceptional = select.select([stembotConn], [], [], 0)
        
        for a in readable:
            if a == stembotConn: # If stembot activity
                data = stembotConn.recv(1024)
                #print_voltage(data)
        sleep(.01)

    stembotConn.close()


if __name__ == '__main__': main()