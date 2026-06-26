#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import array
import math
from std_msgs.msg import Float64MultiArray
import numpy as np


class IK_Slover(Node):

    def __init__(self):
        super().__init__('get_servo_angle')

        self.d1 = 0.05
        self.l2 = math.sqrt((0.236815 * 0.236815) + (0.0300024 * 0.0300024))
        self.l3 = 0.28015

        # Subscriber
        self.coord_sub = self.create_subscription(
            Float64MultiArray, 'send_coord', self.timer_callback, 10
        )

        # Publisher
        self.publish_servo_angle = self.create_publisher(
            Float64MultiArray, 'joint_angle', 10
        )

    def timer_callback(self, msg):

        coord = Float64MultiArray()
        coord = msg.data

        raw_x = coord[0]
        raw_y = coord[1]

        self.get_logger().info(f'pixel raw x,y: {raw_x} , {raw_y}')

        goal_x, goal_y = self.get_distance(raw_x, raw_y)
        self.get_logger().info(f'Coordinates x,y: {goal_x} , {goal_y}')

        self.X_Target = goal_x
        self.Y_Target = goal_y
        self.Z_Target = -0.02

        angles = Float64MultiArray()

        result = self.slove_ik()
        if result is None:
            return

        theta1, theta2, theta3 = result

        b = round(theta1, 3)
        s = -round(theta2, 3)
        e = round(theta3, 3)

        angles.data = [b, s, e]

        self.publish_servo_angle.publish(angles)
        self.get_logger().info(f'Angles : {angles.data}')

    def get_distance(self, x, y):

        x = (x * 0.01 * 0.124)
        y = (y * 0.01 * 0.124)

        self.get_logger().info(f'get_distance x,y: {x} , {y}')

        A = np.array([[0, -1, 0, 0.455], [-1, 0, 0, 0.21], [0, 0, -1, 0], [0, 0, 0, 1]])
        B = np.array([[x], [y], [0], [1]])

        C = A @ B

        x_tar = float(C[0])
        y_tar = float(C[1]) + 0.02

        self.get_logger().info(f'Calculated x,y: {x_tar} , {y_tar}')

        return x_tar, y_tar

    def slove_ik(self):

        q1 = math.atan2(self.Y_Target, self.X_Target)
        r = math.sqrt((self.X_Target * self.X_Target) + (self.Y_Target * self.Y_Target))
        zp = self.Z_Target - self.d1

        c3 = (((r * r) + (zp * zp) - (self.l2 * self.l2)
               - (self.l3 * self.l3))
              / (2 * self.l2 * self.l3))

        if abs(c3) > 1:
            self.get_logger().info("Wrong Coordinates")
            return

        s3 = math.sqrt(1 - (c3 * c3))
        q3 = math.atan2(s3, c3)

        q2 = math.atan2(zp, r) - math.atan2(
            (self.l3 * s3),
            (self.l2 + (self.l3 * c3))
        )

        return q1, q2, q3


def main(args=None):
    rclpy.init(args=args)
    ikslover_angle = IK_Slover()
    rclpy.spin(ikslover_angle)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ikslover_angle.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
