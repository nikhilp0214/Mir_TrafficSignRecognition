#!/usr/bin/env python

import datetime
import os
import cv2
import time
import rospy
import sys
import numpy as np
from bolt_msgs.msg import Control
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from image_converter import ImageConverter
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess
from darknet_ros_msgs.msg import BoundingBoxes
from darknet_ros_msgs.msg import BoundingBox
xMin = 0
yMin = 380
xMax = 800
yMax = 800
class NeuralControl:
    def __init__(self):
        rospy.init_node('controller')
        self.ic = ImageConverter()
        self.image_process = ImageProcess()
        self.rate = rospy.Rate(10)
        self.drive= DriveRun(sys.argv[1])
        rospy.Subscriber('/bolt/front_camera/image_raw', Image, self.controller_cb)
	global sign 	
	sign='none'
        value=rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes, speed_controller)
        self.image = None
        self.image_processed = False


    def controller_cb(self, image): 
        img = self.ic.imgmsg_to_opencv(image)
        #print "rosimage converted to opencv image"
	cropImg = img[yMin:yMax,xMin:xMax]
        #print "image cropped"
        img = cv2.resize(cropImg,(200,66))
        #print "image resized"
        self.image = self.image_process.process(img)
        #print "image normalized"
        self.image_processed = True


def speed_controller(data):
	stop ='stop_sign'
	ped = 'pedestrain_walk'
	park = 'parking'
	right = 'right_turn'
	left = 'left_turn'
	yeld = 'yield'
	spd_10 = 'speed_10'
	spd_15 = 'speed_15'
	spd_20 = 'speed_20' 
	spd_25 = 'speed_25'
	box_data=data.bounding_boxes
	#box_data1=list(box_data)
	#print(box_data[0])
	global sign
	sign=(box_data[0].Class)
	boundx_1=(box_data[0].xmin)
	boundy_1=(box_data[0].ymin)
	boundx_2=(box_data[0].xmax)
	boundy_2=(box_data[0].ymax)

	return boundx_1, boundy_1, boundx_2, boundy_2, sign
	

	#print(type(data.bounding_boxes))

if __name__ == "__main__":
    try:
        neural_control = NeuralControl()
        #joy_data = Control()	
        #joy_data.throttle = 1
        #joy_pub = rospy.Publisher('/bolt', Control, queue_size = 10)
        while not rospy.is_shutdown():
            if neural_control.image_processed == True:
                prediction = neural_control.drive.run(neural_control.image)
                #sign = speed_controller()
                #sign = sign[0]
		#print(sign[0])

		joy_pub = rospy.Publisher('/bolt', Control, queue_size = 10)
	        rate = rospy.Rate(28)
		print(sign)
      	  	joy_data = Control()
                joy_data.steer = prediction
		#detection_data[0]
		#detection_data=speed_controller()
       	        if (sign == 'stop_sign'):
			joy_data.throttle = 0.0
			print(joy_data.throttle)
			print('Stop sign !!')
	        elif (sign == 'ped'):
			joy_data.throttle = 0.0
			print(joy_data.throttle)
			print('look for pedestrains ahead!!!!')
	        elif (sign == 'yield'):
			joy_data.throttle = 0.0
			print(joy_data.throttle)
			print('yelid for moving cars !!!')
	        elif (sign == 'speed_25'):
			joy_data.throttle = 0.8
			print(joy_data.throttle)
			print('speed 25kmph')
	        elif (sign == 'speed_20'):
			joy_data.throttle = 0.6
			print(joy_data.throttle)
			print('speed 20kmph')
	        elif (sign == 'speed_15'):
			joy_data.throttle = 0.4
			print(joy_data.throttle)
			print('speed 15kmph')
	        elif (sign == 'speed_10'):
			joy_data.throttle = 0.2
			print(joy_data.throttle)
			print('speed 10kmph')
	        elif (sign == 'ledt_turn'):
			print('left turn ahead')
	        elif (sign == 'right_turn'):
			print('right turn ahead')
	        elif (sign == 'parking'):
			print('Parking space')
                else:
                        joy_data.throttle = sys.argv[2]
        	joy_pub.publish(joy_data)
                print(prediction)
		print(joy_data.throttle)
                neural_control.image_processed = False
                neural_control.rate.sleep()

    except KeyboardInterrupt:
	   print ('\nShutdown requested. Exiting...')