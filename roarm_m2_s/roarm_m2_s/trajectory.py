#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
import json
import serial
import time
import numpy as np

ser = serial.Serial("/dev/ttyUSB0", 115200)


class Trajectory(Node):

    def __init__(self):
        super().__init__('to_object_pose_cubic_traj')

        self.tar_ang_sub = self.create_subscription(
            Float64MultiArray, 'joint_angle', self.listener_callback, 10)

        self.TimeDuration = 9
        self.dt = 0.02
        self.set_of_pts = self.TimeDuration / self.dt

        self.b_init = 0
        self.s_init = 0
        self.e_init = 1.57

    def listener_callback(self, msg):

        self.init_pose_angle()
        time.sleep(5)
        ang = Float64MultiArray()
        ang = msg.data

        self.b_goal = ang[0]
        self.s_goal = ang[1]
        self.e_goal = ang[2]

        # calculate coefficients
        # base
        c0_base, c1_base, c2_base, c3_base = self.cal_coefficients(
            self.b_goal, self.b_init, self.TimeDuration)
        # shoulder
        c0_shoulder, c1_shoulder, c2_shoulder, c3_shoulder = self.cal_coefficients(
            self.s_goal, self.s_init, self.TimeDuration)
        # elbow
        c0_elbow, c1_elbow, c2_elbow, c3_elbow = self.cal_coefficients(
            self.e_goal, self.e_init, self.TimeDuration)

        self.t = 0
        self.count = 0

        self.start_time = time.time()
        self.next_time = self.start_time

        while self.t < self.TimeDuration:

            self.t = self.dt * self.count
            self.count += 1

            # self.get_logger().info(f'Inside the loop')

            # base
            theta_b, vel_b, acc_b = self.cal_tva(c0_base, c1_base, c2_base, c3_base, self.t)
            # self.tar_pose_angle(1, theta_b, 0, 3)
            # shoulder
            theta_s, vel_s, acc_s = self.cal_tva(
                c0_shoulder, c1_shoulder, c2_shoulder, c3_shoulder, self.t)
            # self.tar_pose_angle(2, theta_s, 0, 3)
            # elbow
            theta_e, vel_e, acc_e = self.cal_tva(c0_elbow, c1_elbow, c2_elbow, c3_elbow, self.t)
            # self.tar_pose_angle(3, theta_e, 0, 3)
            self.new_pose_angle(theta_b, theta_s, theta_e)

            self.next_time += self.dt
            self.sleep_time = self.next_time - time.time()
            if self.sleep_time > 0:
                time.sleep(self.sleep_time)

        time.sleep(5)
        self.grab_angle()
        time.sleep(10)
        self.pick_pose_angle()
        time.sleep(10)
        self.place_pose_angle()
        time.sleep(10)
        self.open_angle()
        time.sleep(5)
        self.init_pose_angle()

    def cal_coefficients(self, q0, qi, total_t):
        c0 = qi
        c1 = 0
        c2 = (3 * (q0 - qi)) / (total_t * total_t)
        c3 = (-2 * (q0 - qi)) / (total_t * total_t * total_t)
        return c0, c1, c2, c3

    def cal_tva(self, c0, c1, c2, c3, dt):
        theta = c0 + (c1 * dt) + (c2 * dt * dt) + (c3 * dt * dt * dt)
        velocity = c1 + (c2 * 2 * dt) + (c3 * 3 * dt * dt)
        acc = (2 * c2) + (6 * c3 * dt)
        return theta, velocity, acc

    def tar_pose_angle(self, joint, rad, spd, acc):

        data = json.dumps({'T': 101,
                           'joint': joint,
                           'rad': rad,
                           'spd': spd,
                           'acc': acc}) + "\n"
        ser.write(data.encode())

    def init_pose_angle(self):

        data = json.dumps({'T': 102,
                           'base': 0,
                           'shoulder': 0,
                           'elbow': 1.57,
                           'hand': 2.093,
                           'spd': 0,
                           'acc': 5}) + "\n"
        ser.write(data.encode())

    def new_pose_angle(self, x, y, z):

        data = json.dumps({'T': 102,
                           'base': x,
                           'shoulder': y,
                           'elbow': z,
                           'hand': 2.093,
                           'spd': 0,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def grab_angle(self):
        data = json.dumps({'T': 101,
                           'joint': 4,
                          'rad': 3.05,
                           'spd': 1,
                           'acc': 3}) + "\n"
        ser.write(data.encode())

    def pick_pose_angle(self):

        data = json.dumps({'T': 102,
                           'base': 0,
                           'shoulder': 0,
                           'elbow': 1.57,
                           'hand': 3.05,
                           'spd': 0,
                           'acc': 5}) + "\n"
        ser.write(data.encode())

    def place_pose_angle(self):

        data = json.dumps({'T': 102,
                           'base': -0.5,
                           'shoulder': 0.67,
                           'elbow': 2.24,
                           'hand': 3.05,
                           'spd': 0,
                           'acc': 2}) + "\n"
        ser.write(data.encode())

    def open_angle(self):
        data = json.dumps({'T': 101,
                           'joint': 4,
                           'rad': 2,
                           'spd': 0,
                           'acc': 5}) + "\n"
        ser.write(data.encode())


def main(args=None):
    rclpy.init(args=args)
    tra = Trajectory()
    rclpy.spin_once(tra)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tra.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
