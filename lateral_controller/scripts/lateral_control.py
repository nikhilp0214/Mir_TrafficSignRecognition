#!/usr/bin/env python

import datetime
import os
import cv2
import time
import rospy
import sys
import numpy as np
import time
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
	sign=None
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
	global sign,boundx_1,boundy_1,boundx_2,boundy_2
	sign=(box_data[0].Class)
	boundx_1=(box_data[0].xmin)
	boundy_1=(box_data[0].ymin)
	boundx_2=(box_data[0].xmax)
	boundy_2=(box_data[0].ymax)
	minx=(boundx_2-boundx_1)
	miny=(boundy_2-boundy_1)

	return boundx_1, boundy_1, boundx_2, boundy_2, sign, minx, miny
	

	#print(type(data.bounding_boxes))

if __name__ == "__main__":
    try:
	boundx_1=0
	boundx_2=0
	boundy_1=0
	boundy_2=0
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
		#print(sign)
      	  	joy_data = Control()
                joy_data.steer = prediction
		#detection_data[0]
		#detection_data=speed_controller()
               # print(boundx_1)
                #print(boundx_2)
                #print(boundy_1)
                #print(boundy_2)
                #print(boundx_2-boundx_1)
                #print(boundy_2-boundy_1)
        	if ((boundx_2-boundx_1) > 50 and (boundy_2-boundy_1) > 40):
	            print('sign ahead')
		    print(sign)
       	            if (sign == 'stop_sign'):
			    print('Stop sign !!')
			    for i in range (6):
				joy_data.brake = 1.0
				joy_pub.publish(joy_data)
				time.sleep(1)
			    if (joy_data.brake == 1.0):
				#for j in range (5):
					joy_data.brake = 0
					joy_pub.publish(joy_data)
					joy_data.throttle = 1.0
					joy_pub.publish(joy_data)
					sign = None
					time.sleep(5)
			    print(joy_data.throttle)
	            if (sign == 'ped'):
			    joy_data.throttle = 0.0
			    print(joy_data.throttle)
			    print('look for pedestrains ahead!!!!')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'yield'):
			    joy_data.throttle = 0.0
			    print(joy_data.throttle)
			    print('yelid for moving cars !!!')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'speed_25'):
			    joy_data.throttle = 0.5
			    print(joy_data.throttle)
			    print('speed 25kmph')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'speed_20'):
			    joy_data.throttle = 0.4
			    print(joy_data.throttle)
			    print('speed 20kmph')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'speed_15'):
			    joy_data.throttle = 0.3
			    print(joy_data.throttle)
			    print('speed 15kmph')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'speed_10'):
			    joy_data.throttle = 0.2
			    print(joy_data.throttle)
			    print('speed 10kmph')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'ledt_turn'):
			    print('left turn ahead')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'right_turn'):
			    print('right turn ahead')
		    	    joy_pub.publish(joy_data)
	            elif (sign == 'parking'):
			    print('Parking space')
		    	    joy_pub.publish(joy_data)
                    elif (sign==None):   
                            print(' none  ')
                           # joy_data.throttle = sys.argv[2]
			    joy_data.throttle = 0.3
		    	    joy_pub.publish(joy_data)	     
 		else:
                    joy_data.throttle = 0.2
		    joy_pub.publish(joy_data)	     

                print(prediction)
		#print(joy_data.throttle)
                neural_control.image_processed = False
                neural_control.rate.sleep()

    except KeyboardInterrupt:
	   print ('\nShutdown requested. Exiting...')
