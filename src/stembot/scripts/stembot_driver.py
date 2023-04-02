#! /usr/bin/env python3

#
# stembot topside control script
#

import select
import socket
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

THRUSTER_NEUTRAL = 1500 #us
THRUSTER_MAX     = 2200 
THRUSTER_MIN     = 800

def truncate(value, min, max):
    ret = value
    if ret < min:
        ret = min
    elif ret > max:
        ret = max
    
    return ret

class StembotDriver(Node):
    def __init__(self):
        super().__init__("stembot_driver")
        self.declare_parameter("address", "stembot-phoenix.local")
        
        #connect to stembot
        self.connected = False
        
        #joy subscriber for controller info
        self.joySub = self.create_subscription(Joy, "joy", self.joyCb, 10)
        
        #connection timer that runs every second until stembot connects
        self.connector = self.create_timer(1, self.connectCb)
        
        #timer that receives data from the stembot
        self.monitor = self.create_timer(0.05, self.timerCb)
        
        self.conn = None
        self.battery = 0
        
    
    def shutdown(self):
        if self.conn is not None:
            self.conn.close()
        
        
    def joyCb(self, msg):
        if self.connected:
            #triggers are (trigger value + 1) / 2 because joy_node reports them as -1 to 1. we want them from 0 to 1
            heave_front = 1 - ((msg.axes[5] + 1) / 2) # right trigger
            heave_aft = 1 - ((msg.axes[2] + 1) / 2) # left trigger
            surge_port = msg.axes[1] # left joystick
            surge_starboard = msg.axes[4] # right joystick
            
            thrustor_range = (THRUSTER_MAX - THRUSTER_MIN) / 2
            ps = (thrustor_range * surge_port) + THRUSTER_NEUTRAL
            ss = (thrustor_range * surge_starboard) + THRUSTER_NEUTRAL
            fh = (thrustor_range * heave_front) + THRUSTER_NEUTRAL
            ah = (thrustor_range * heave_aft) + THRUSTER_NEUTRAL
            
            ss = truncate(ss, THRUSTER_MIN, THRUSTER_MAX)
            fh = truncate(fh, THRUSTER_MIN, THRUSTER_MAX)
            ps = truncate(ps, THRUSTER_MIN, THRUSTER_MAX)
            ah = truncate(ah, THRUSTER_MIN, THRUSTER_MAX)
            
            print(ps)
            print(ss)
            print(fh)
            print(ah)
            print()
            
            data = bytearray()
            data.append(int(ps/256))
            data.append(int(ps%256))
            data.append(int(ss/256))
            data.append(int(ss%256))
            data.append(int(fh/256))
            data.append(int(fh%256))
            data.append(int(ah/256))
            data.append(int(ah%256))
            self.conn.sendall(data)
    
    
    def connectCb(self):
        if not self.connected:
            try:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.settimeout(1)
                self.addr = self.get_parameter("address").value
                self.get_logger().info(f"Connecting to {self.addr}")
                self.conn.connect((self.addr, 50000))
                self.connected = True
                
                #stop timer because we dont want to continue connecting
                self.connector.cancel()
                self.get_logger().info("Stembot connected! Press ctrl+C to quit.")
            except Exception as ex:
                self.get_logger().error(f"Could not connect to stembot: {ex}")
                time.sleep(1)
                
    
    def print_voltage(self, value):
        global battery
        value = int(value.split(b"\n")[-2])
        percent = (value * 12.35 / 910 - 11.1) / 1.5
        if battery == 0:
            battery = percent
            
        battery = .999 * battery + .001 * percent
        percent=str(round(battery * 100, 2))
        self.get_logger().info(f"Battery: {percent}%")
    
    
    def timerCb(self):
        if self.connected:
            readable, writable, exceptional = select.select([self.conn], [], [], 0)
            
            for a in readable:
                if a == self.conn: # If stembot activity
                    data = self.conn.recv(1024)
                    #print_voltage(data)


def main(args = None):
    rclpy.init(args = args)
    driver = StembotDriver()
    rclpy.spin(driver)
    driver.shutdown()
    rclpy.shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stembot driver was interrupted.")
