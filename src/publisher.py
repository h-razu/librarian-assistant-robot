#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose2D  # Message type for (x, y, yaw)

# Mapping numbers to (x, y, yaw) values
shelf_map = {
    1: (1.70, -3.49, 0),
    2: (1.70, -1.51, 0),
    3: (1.70, 0.47, 0),
    4: (1.70, 2.60, 0),
    5: (1.70, 4.58, 0),

    6: (0.8, -2.93, 0),
    7: (0.8, -1.11, 0),
    8: (0.8, -0.27, 0),
    9: (0.8, 1.11, 0),
    10: (0.8, 2.93, 0),

    11: (-0.8, -2.93, 0),
    12: (-0.8, -1.11, 0),
    13: (-0.8, -0.27, 0),
    14: (-0.8, 1.11, 0),
    15: (-0.8, 2.93, 0),

    16: (-1.70, -3.49, 0),
    17: (-1.70, -1.51, 0),
    18: (-1.70, -0.47, 0),
    19: (-1.70, 2.45, 0),
    20: (-1.70, 4.43, 0),

}

def goal_publisher():
    # Initialize the ROS node
    rospy.init_node('goal_publisher', anonymous=True)

    # Create a publisher for the /move_goal topic
    pub = rospy.Publisher('/move_goal', Pose2D, queue_size=10)

    # Set the rate of publishing (e.g., 1Hz)
    rate = rospy.Rate(1)

    # Continuously ask for user input and publish the goal
    while not rospy.is_shutdown():
        # Ask the user for shelf number (1 to 20)
        try:
            goal_number = int(input("Enter shelf number (1-20): "))
            if goal_number < 1 or goal_number > 20:
                rospy.logerr("Invalid shelf number. Please enter a number between 1 and 20.")
                continue
        except ValueError:
            rospy.logerr("Invalid input. Please enter a number between 1 and 20.")
            continue

        # Get corresponding goal (x, y, yaw) from the dictionary
        goal_x, goal_y, goal_yaw = shelf_map[goal_number]

        # Create the Pose2D message
        goal = Pose2D()
        goal.x = goal_x
        goal.y = goal_y
        goal.theta = goal_yaw

        # Log and publish the goal
        rospy.loginfo(f"Publishing goal: x={goal.x}, y={goal.y}, yaw={goal.theta}")
        pub.publish(goal)

        rate.sleep()

if __name__ == '__main__':
    try:
        goal_publisher()
    except rospy.ROSInterruptException:
        pass

