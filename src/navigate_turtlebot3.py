#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionResult

# Define the nine locations as PoseStamped messages
locations = {
    1 : (1.40, -3.0, 0.0),
    2 : (1.10, -3.0, 0.0),
    3 : (1.40, 0.0, 0.0),
    4 : (1.10, 0.0, 0.0),
    5 : (1.40, 3.0, 0.0),
    6 : (1.10, 3.0, 0.0),
    7 : (-1.10, 3.0, 0.0),
    8 : (-1.40, 3.0, 0.0),
    9 : (-1.10, 0.0, 0.0),
   10 : (-1.40, 0.0, 0.0),
   11 : (-1.10, -3.0, 0.0),
   12 : (-1.40, -3.0, 0.0)
}

# Define the initial position
initial_position = PoseStamped(pose=Pose(position=Point(x=1.25, y=-4.0, z=0.0), orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)))

goal_reached = False  # Flag to track if the robot has reached the goal

def goal_status_callback(msg):
    """Callback to check if the robot reached the goal."""
    global goal_reached
    for status in msg.status_list:
        if status.status == 3:  # Status 3 means "Goal Reached"
            goal_reached = True
            rospy.loginfo("Goal reached!")

def send_goal(goal_pose):
    """Send the robot to the specified goal."""
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.sleep(1)  # Wait for the publisher to connect
    rospy.loginfo(f"Sending robot to position: ({goal_pose.pose.position.x}, {goal_pose.pose.position.y})")
    pub.publish(goal_pose)

def main():
    global goal_reached
    rospy.init_node('turtlebot3_navigation')
    rospy.Subscriber('/move_base/status', GoalStatusArray, goal_status_callback)

    print("Welcome to the TurtleBot3 Navigation Program!")
    print("Enter a number (1-9) to select a location. Type 'exit' to quit.")
    
    while not rospy.is_shutdown():
        try:
            user_input = input("Enter location number (1-9): ")
            if user_input.lower() == 'exit':
                print("Exiting program.")
                break
            
            location_number = int(user_input)
            if location_number not in locations:
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            
            # Send the robot to the selected location
            goal_reached = False  # Reset the flag
            send_goal(locations[location_number])
            
            # Wait for the robot to reach the goal
            rospy.loginfo("Waiting for the robot to reach the goal...")
            while not goal_reached and not rospy.is_shutdown():
                rospy.sleep(0.5)
            
            # Once the goal is reached, return to the initial position
            rospy.loginfo("Returning to the initial position.")
            goal_reached = False  # Reset the flag for returning
            send_goal(initial_position)
            
            # Wait for the robot to return to the initial position
            while not goal_reached and not rospy.is_shutdown():
                rospy.sleep(0.5)

            rospy.loginfo("Robot returned to the initial position.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except rospy.ROSInterruptException:
            print("ROS node interrupted. Exiting program.")
            break

if __name__ == '__main__':
    main()

