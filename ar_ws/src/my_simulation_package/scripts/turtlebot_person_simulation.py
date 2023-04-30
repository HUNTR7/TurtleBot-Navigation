#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Twist

class PersonController:
    def __init__(self):
        rospy.init_node('person_controller')

        self.pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
        rospy.Subscriber('/cmd_vel', Twist, self.cmdVelCallback)

        self.state = ModelState()
        self.state.model_name = 'person'
        self.state.reference_frame = 'world'
        self.state.pose.position.x = 1
        self.state.pose.position.y = 0
        self.state.pose.position.z = 0.5

        self.vel = 0

        self.rate = rospy.Rate(10)

    def cmdVelCallback(self, msg):
        self.vel = msg.linear.x

    def run(self):
        while not rospy.is_shutdown():
            self.state.pose.position.x += self.vel * self.rate.sleep_dur.to_sec()
            self.pub.publish(self.state)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = PersonController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
