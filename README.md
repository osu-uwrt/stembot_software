OSU UWRT STEMbot
================

Contents
--------

* pi-driver - Starts the motor driver.
* ps3-driver - Starts the controller.
* reset-cam - Restarts the camera driver.

Usage
-----

SSH into the Raspberry Pi:

    sudo ./pi-driver

On the topside computer:

    sudo ./ps3-driver

Navigate to: [http://raspberrypi:8080](http://raspberrypi:8080)

Troubleshooting
---------------

If there's trouble with the camera:

    ./reset-camera

Installation
------------

**Controls**

    git clone https://github.com/osu-uwrt/stembot.git

**Camera:**

See: [Linux Projects](http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14)
