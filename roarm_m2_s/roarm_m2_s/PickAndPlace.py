#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
import json
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)


class PickAndPlace(Node):

    def __init__(self):
        super().__init__('to_object_pose')

        self.tar_ang_sub = self.create_subscription(
            Float64MultiArray, 'joint_angle', self.listener_callback, 10)

    def listener_callback(self, msg):

        ang = Float64MultiArray()
        ang = msg.data

        b = str(ang[0])
        s = str(ang[1])
        e = str(ang[2])

        # time.sleep(15)
        # self.get_logger().info("Init Pose")
        self.init_pose_angle()
        time.sleep(15)
        self.get_logger().info("Target Pose")
        self.tar_pose_angle(b, s, e)
        time.sleep(15)
        self.get_logger().info("Grab Pose")
        self.grab_angle()
        time.sleep(15)
        self.get_logger().info("Place Pose")
        self.place_pose_angle()
        time.sleep(15)
        self.get_logger().info("Open Pose")
        self.open_angle()
        time.sleep(15)
        self.get_logger().info("Init Pose")
        self.init_pose_angle()
        time.sleep(15)

    def tar_pose_angle(self, x, y, z):

        data = json.dumps({'T': 102,
                           'base': x,
                           'shoulder': y,
                           'elbow': z,
                           'hand': 1.57,
                           'spd': 5,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def grab_angle(self):
        data = json.dumps({'T': 101,
                           'joint': 4,
                           'rad': 3.05,
                           'spd': 5,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def init_pose_angle(self):

        data = json.dumps({'T': 122,
                           'b': 0,
                           's': 0,
                           'e': 90,
                           'h': 120,
                           'spd': 5,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def place_pose_angle(self):

        data = json.dumps({'T': 102,
                           'base': 0.77,
                           'shoulder': 0.67,
                           'elbow': 2.24,
                           'hand': 3.05,
                           'spd': 5,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def open_angle(self):
        data = json.dumps({'T': 101,
                           'joint': 4,
                           'rad': 2,
                           'spd': 5,
                           'acc': 3}) + "\n"
        ser.write(data.encode())


def main(args=None):
    rclpy.init(args=args)
    pnp = PickAndPlace()
    rclpy.spin_once(pnp)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pnp.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
