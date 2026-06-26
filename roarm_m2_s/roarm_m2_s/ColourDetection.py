#! /usr/bin/env python3
import cv2
import rclpy
import numpy as np
from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge


class SubcriberNodeClass(Node):

    def __init__(self):
        super().__init__('colour_detection_node')
        self.bridgeObject = CvBridge()
        self.topicNameFrames = 'topic_camera_image'
        self.topicNameFramePub = 'camera_colour_detection'
        self.queueSize = 20

        self.publisher = self.create_publisher(Image, self.topicNameFramePub, self.queueSize)

        self.subscriber = self.create_subscription(
            Image, self.topicNameFrames, self.listener_callbackFunction, self.queueSize)
        self.subscriptions

    def listener_callbackFunction(self, imageMessage):

        self.get_logger().info('Detecting Colour and generating mask')
        imageFrame = self.bridgeObject.imgmsg_to_cv2(imageMessage)
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        # Set range for RGB color
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        green_lower = np.array([35, 100, 100], np.uint8)
        green_upper = np.array([85, 255, 255], np.uint8)
        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)

        # define mask
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # to detect RGB colour
        kernal = np.ones((5, 5), "uint8")
        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 0, 255), 2)

                cv2.putText(imageFrame, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))
        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Green Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 255, 0))
        # Creating contour to track Blue color
        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (225, 0, 0), 2)

                cv2.putText(imageFrame, "Blue Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 0, 0))
        cv2.imshow("Camera Video", imageFrame)
        cv2.waitKey(1)
        # MaskedImage = self.bridgeObject.cv2_to_imgmsg(imageFrame)
        # self.publisher.publish(MaskedImage)


def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = SubcriberNodeClass()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
