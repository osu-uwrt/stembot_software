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

    roslaunch stembot stem.launch address:=stembot-phoenix.local

Start the pi code if it isnt running (should automatically):

    ssh pi@stembot-botname.local
    sudo python go.py
    

Pi Setup
--------

1. Install raspbian
2. Set hostname to stembot-botname
3. Place go.py in the home directory of pi
4. Install servo hat library: `sudo pip3 install adafruit-circuitpython-pca9685`
5. Place stembot.servce in `/etc/systemd/system`
6. Run `systemd enable stembot.service` to enable running at boot
7. Reboot the raspberry pi
