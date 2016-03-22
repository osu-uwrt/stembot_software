#include "ros/ros.h"
#include "sensor_msgs/Joy.h"
#include "geometry_msgs/Wrench.h"

class Teleop
{
  private:
    ros::NodeHandle nh;
    ros::Publisher wrench_pub;
    ros::Subscriber sixaxis_sub;
    geometry_msgs::Wrench wrench;

  public:
    Teleop();
    void sixaxis_callback(const sensor_msgs::Joy::ConstPtr& joy);
    void loop();
};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "teleop");
  Teleop teleop;
  teleop.loop();
}

Teleop::Teleop()
{
  sixaxis_sub = nh.subscribe<sensor_msgs::Joy>("joy", 1, &Teleop::sixaxis_callback, this);
  wrench_pub = nh.advertise<geometry_msgs::Wrench>("body_wrench", 1);
}

void Teleop::sixaxis_callback(const sensor_msgs::Joy::ConstPtr& joy)
{
  wrench.force.x = joy->axes[3] * 5;
  wrench.force.y = joy->axes[2] * 5;
  wrench.force.z = joy->axes[1] * 5;

  wrench.torque.x = 0;
  wrench.torque.y = 0;
  wrench.torque.z = 0;

  wrench_pub.publish(wrench);
}

void Teleop::loop()
{
  ros::Rate rate(30);
  while(ros::ok())
  {
    ros::spinOnce();
    rate.sleep();
  }
}
