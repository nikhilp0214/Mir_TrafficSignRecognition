#!/usr/bin/env python

import rospy
import cv2
import os
import numpy as np
import datetime
import time
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from image_converter import ImageConverter
from std_msgs.msg import String
from bolt_msgs.msg import Control
vehicle_steer = 0
vehicle_vel = 0

ic = ImageConverter()
#path = '/home/nikhil/dtec_mc/Data_collection/' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
path = sys.argv[1] + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
if os.path.exists(path):
    print('path exists. continuing...')
else:
    os.makedirs(path)

text = open(str(path) + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".txt", "w+")


def vehicle_param(value):
    global vehicle_vel, vehicle_steer
    vehicle_vel = value.throttle
    vehicle_steer = value.steer
    #return (vehicle_vel, vehicle_steer)

def recorder(data):
    img = ic.imgmsg_to_opencv(data)
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    cv2.imwrite(str(path) + str(time_stamp) + '.jpg',img)
    text.write(str(time_stamp) + '\t' + str(vehicle_steer) + '\t' + str(vehicle_vel) + "\r\n")

def main():
   rospy.init_node('data_collection')
   rospy.Subscriber('/bolt', Control, vehicle_param)
   rospy.Subscriber('/bolt/front_camera/image_raw', Image, recorder)
   rospy.spin()

if __name__ == '__main__':
    main()
