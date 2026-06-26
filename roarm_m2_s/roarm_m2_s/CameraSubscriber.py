#! /usr/bin/env python3
import cv2
import rclpy
from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge


class SubcriberNodeClass(Node):

    def __init__(self):
        super().__init__('cam_sub_node')
        self.bridgeObject = CvBridge()
        self.topicNameFrames = 'camera_colour_detection'
        self.queueSize = 20
        self.subscriber = self.create_subscription(
            Image, self.topicNameFrames, self.listener_callbackFunction, self.queueSize)
        self.subscriptions

    def listener_callbackFunction(self, imageMessage):

        self.get_logger().info('Subscribing image number')
        openCVImage = self.bridgeObject.imgmsg_to_cv2(imageMessage)
        cv2.imshow("Camera Video", openCVImage)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = SubcriberNodeClass()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
