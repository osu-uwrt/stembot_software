////////////////////////////
// Require/Import/Include //
////////////////////////////

var dgram = require('dgram');
var fs = require('fs');

///////////////
// Constants //
///////////////

var MY_IP = '192.168.1.71';

///////////////////////
// Port Thruster PWM //
///////////////////////

var duty9_22 = fs.createWriteStream('/sys/devices/ocp.3/pwm_test_P9_22.15/duty');
var udp9_22 = dgram.createSocket('udp4');
udp9_22.bind(9022,MY_IP);
udp9_22.on("message", function (msg, rinfo) {
	console.log("Port 9022 received: " + msg + " from " +
		rinfo.address + ":" + rinfo.port);
	duty9_22.write(msg);
  udp9_22.send(msg, 0, msg.length, rinfo.port, rinfo.address, function() {
    console.log("Port 9022 replied.");
});
});
udp9_22.on("listening", function () {
	var address = udp9_22.address();
	console.log("Port 9022 listening on " +
		address.address + ":" + address.port);
});
udp9_22.on("close", function () {
	console.log("Port 9022 closed.");
});
udp9_22.on("error", function (err) {
	console.log("Port 9022 error:\n" + err.stack);
	udp9_22.close();
});

///////////////////////
// Stbd Thruster PWM //
///////////////////////

var duty9_14 = fs.createWriteStream('/sys/devices/ocp.3/pwm_test_P9_14.16/duty');
var udp9_14 = dgram.createSocket('udp4');
udp9_14.bind(9014,MY_IP);
udp9_14.on("message", function (msg, rinfo) {
	console.log("Port 9014 received: " + msg + " from " +
		rinfo.address + ":" + rinfo.port);
	duty9_14.write(msg);
	udp9_14.send(msg, 0, msg.length, rinfo.port, rinfo.address, function() {
		console.log("Port 9014 replied.");
});
});
udp9_14.on("listening", function () {
	var address = udp9_14.address();
	console.log("Port 9014 listening on " +
		address.address + ":" + address.port);
});
udp9_14.on("close", function () {
	console.log("Port 9014 closed.");
});
udp9_14.on("error", function (err) {
	console.log("Port 9014 error:\n" + err.stack);
	udp9_14.close();
});

///////////////////////////
// Vertical Thruster PWM //
///////////////////////////

var duty9_42 = fs.createWriteStream('/sys/devices/ocp.3/pwm_test_P9_42.18/duty');
var udp9_42 = dgram.createSocket('udp4');
udp9_42.bind(9042,MY_IP);
udp9_42.on("message", function (msg, rinfo) {
	console.log("Port 9042 received: " + msg + " from " +
		rinfo.address + ":" + rinfo.port);
	duty9_42.write(msg);
	udp9_42.send(msg, 0, msg.length, rinfo.port, rinfo.address, function() {
		console.log("Port 9042 replied.");
});
});
udp9_42.on("listening", function () {
	var address = udp9_42.address();
	console.log("Port 9042 listening on " +
		address.address + ":" + address.port);
});
udp9_42.on("close", function () {
	console.log("Port 9042 closed.");
});
udp9_42.on("error", function (err) {
	console.log("Port 9042 error:\n" + err.stack);
	udp9_42.close();
});
