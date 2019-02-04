STEMbot Documentation
====================

Contents
--------

* go - Pi side motor controller.
* STEMbot-driver - Listens to controllers and tells STEMbot what to do.

Usage
-----

Power STEMbot:

	Plug in battery to ESCs
	Plug portable charger into pi
	Close STEMbot and plug into one of the teams's routers

Start the controller:

    python STEMbot-driver.py

Start the pi code if it isnt running (should automatically):

    ssh pi@raspberrypi
    sudo python go.py
    

Pi Setup
--------

1. Install raspbian
2. Set static ip of 192.168.1.112
3. Place go.py in the home directory of pi
4. Setup [maestro driver](https://github.com/FRC4564/Maestro).
5. Add the following to /etc/rc.local to autorun go.py
	exec 2> /tmp/rc.local.log
	exec 1>&2
	echo "rc Started"
	sudo python /home/pi/go.py &
6. Download and install Maestro Control Center(follow instructions on https://www.pololu.com/docs/0J40/3.a)
7. Connect the Maestro to the computer and on the Maestro Control Center in the Channel Settings tab, change the mode of channel 6 to Input and apply settings.
8. Connect the Maestro back to the Raspberry Pi.
