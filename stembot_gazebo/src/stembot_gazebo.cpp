#include "ros/ros.h"
#include "geometry_msgs/Wrench.h"

class Sim
{
  private:
    ros::NodeHandle nh;
    ros::Publisher port_wrench;
    ros::Publisher stbd_wrench;
    ros::Publisher vert_wrench;
    ros::Subscriber wrench_sub;
    geometry_msgs::Wrench wrench_p;
    geometry_msgs::Wrench wrench_s;
    geometry_msgs::Wrench wrench_v;

  public:
    Sim();
    void sim_callback(const geometry_msgs::Wrench::ConstPtr& wrench);
    void loop();
};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "sim");
  Sim sim;
  sim.loop();
}

Sim::Sim()
{
  wrench_sub = nh.subscribe<geometry_msgs::Wrench>("body_wrench", 1, &Sim::sim_callback, this);
  port_wrench = nh.advertise<geometry_msgs::Wrench>("port_thruster_force", 1);
  stbd_wrench = nh.advertise<geometry_msgs::Wrench>("stbd_thruster_force", 1);
  vert_wrench = nh.advertise<geometry_msgs::Wrench>("vert_thruster_force", 1);
}

void Sim::sim_callback(const geometry_msgs::Wrench::ConstPtr& wrench)
{
  wrench_p.force.x = wrench->force.x;
  wrench_s.force.x = wrench->force.y;
  wrench_v.force.z = wrench->force.z;

  port_wrench.publish(wrench_p);
  stbd_wrench.publish(wrench_s);
  vert_wrench.publish(wrench_v);
}

void Sim::loop()
{
  ros::Rate rate(30);
  while(ros::ok())
  {
    ros::spinOnce();
    rate.sleep();
  }
}
