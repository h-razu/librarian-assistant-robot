#!/usr/bin/env python3

import rospy
import sys
import tf
import math
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from scipy.spatial.transform import Rotation as R
from geometry_msgs.msg import Pose2D  # Message type for (x, y, yaw)

class Mover:
    def __init__(self, robot_name):
        # get the name prefix
        self.robot_name = robot_name

    # client that sends our goals to move base
    def movebase_client(self, wanted_x, wanted_y, wanted_yaw):
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        # create goal and fill it with the wanted info
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = wanted_x
        goal.target_pose.pose.position.y = wanted_y

        # initialise rotation from euler angles
        r = R.from_euler('xyz', [0, 0, wanted_yaw], degrees=True)

        # fill our wanted orientation in quaternion
        goal.target_pose.pose.orientation.x = r.as_quat()[0]
        goal.target_pose.pose.orientation.y = r.as_quat()[1]
        goal.target_pose.pose.orientation.z = r.as_quat()[2]
        goal.target_pose.pose.orientation.w = r.as_quat()[3]

        # send the goal
        client.send_goal(goal)
        wait = client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            return client.get_result()

    # send a new goal to the robot
    def sendNewGoal(self, x, y, yaw):
        result = self.movebase_client(x, y, yaw)
        if result:
            rospy.loginfo(f'Goal reached: x={x}, y={y}, yaw={yaw}')
        else:
            rospy.loginfo(f'Failed to reach goal: x={x}, y={y}, yaw={yaw}')

# Callback function for subscriber
def goal_callback(msg):
    rospy.loginfo(f"Received goal: x={msg.x}, y={msg.y}, yaw={msg.theta}")
    mover_object = Mover('Turtlebot3-Burger')
    mover_object.sendNewGoal(msg.x, msg.y, msg.theta)

def main(args):
    # initialize node
    rospy.init_node('mover_node', anonymous=True)

    # get arguments and instantiate object of class
    robot_name = 'Turtlebot3-Burger'

    # create object of class Mover
    mover_object = Mover(robot_name)

    # create subscriber to the /move_goal topic
    rospy.Subscriber('/move_goal', Pose2D, goal_callback)

    rospy.loginfo("Waiting for goals...")
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main(sys.argv)

