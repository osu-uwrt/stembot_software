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
    

Installation
------------

**Code**

    git clone https://github.com/osu-uwrt/stembot.git

	
Pi Setup
--------

1. Install raspbian
2. Set static ip of 192.168.1.112
3. Place go.py in the home directory of pi
4. Setup [maestro driver](https://github.com/FRC4564/Maestro).