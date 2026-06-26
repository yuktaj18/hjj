#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)


class HomePose(Node):

    def __init__(self):
        super().__init__('to_home_pose')
        self.serialpub = self.create_publisher(String, 'home_pose_angle', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        data = json.dumps({'T': 122,
                           'b': 0,
                           's': 0,
                           'e': 170,
                           'h': 180,
                           'spd': 10,
                           'acc': 10}) + "\n"
        ser.write(data.encode())

        self.get_logger().info("Home Pose")


def main(args=None):
    rclpy.init(args=args)
    home_pose = HomePose()
    rclpy.spin_once(home_pose)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    home_pose.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
