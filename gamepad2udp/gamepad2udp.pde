import hypermedia.net.*;
import gamepadd.*;

String ip = "192.168.1.254";

UDP port;
UDP stbd;
UDP vert;

Gamepadd gamepad;

int lv = 0;
int rv = 0;
int rh = 0;

int MIN_DUTY = 1000000;
int STK_SCALE = 500000;
float DEAD_ZONE = 0.1f;

void setup() {
  port = new UDP(this, 9022);
  stbd = new UDP(this, 9014);
  vert = new UDP(this, 9042);

  gamepad = new Gamepadd(this, STK_SCALE, DEAD_ZONE);
}

void draw() {
  port.send(Integer.toString(MIN_DUTY + (rh >= 0 ? rv + rh : rv)), ip, port.port());
  stbd.send(Integer.toString(MIN_DUTY + (rh <= 0 ? rv - rh : rv)), ip, stbd.port());
  vert.send(Integer.toString(MIN_DUTY + lv), ip, vert.port());

  lv = int( gamepad.getLeftVertical() );
  rv = int( gamepad.getRightVertical() );
  rh = int( gamepad.getRightHorizontal() );

  lv = lv >= 0 ? lv : 0;
  rv = rv >= 0 ? rv : 0;
}

