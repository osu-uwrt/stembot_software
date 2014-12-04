import hypermedia.net.*;
import gamepadd.*;

String ip = "192.168.1.100";

UDP port;
UDP stbd;
UDP vert;

Gamepadd gamepad;

int lv = 0;
int rv = 0;
int rh = 0;

void setup() {
  port = new UDP(this, 9022);
  stbd = new UDP(this, 9014);
  vert = new UDP(this, 9042);

  gamepad = new Gamepadd(this, 10, .1);
}

void draw() {
  port.send(Integer.toString(rh >= 0 ? rv + rh : rv), ip, port.port());
  stbd.send(Integer.toString(rh <= 0 ? rv - rh : rv), ip, stbd.port());
  vert.send(Integer.toString(lv), ip, vert.port());

  lv = int( gamepad.getLeftVertical() );
  rv = int( gamepad.getRightVertical() );
  rh = int( gamepad.getRightHorizontal() );

  lv = lv >= 0 ? lv : 0;
  rv = rv >= 0 ? rv : 0;
}

