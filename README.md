## STEMbot
*STEM outreach/education mini-bot.*

**The Underwater Robotics Team**  
The Ohio State University

* `ps3-driver.py`
    * Run this on the topside computer with the PS3 controller plugged in.
    * It will send PS3 controller inputs to the specified address and port `ADDR`
    * Right now, this only uses Y of the left joystick, and X,Y of the right joystick
* `pi-driver.py`
    * Run this on the STEMbot's Raspberry pi.
    * It will listen for the PS3 controls at the specified `ADDR`

![STEMbot](http://underwaterrov.org.ohio-state.edu/img/renders/stembot_180.png)

[Website](http://go.osu.edu/uwrt) | [Documentation](DOC.md) | [License](LICENSE)
