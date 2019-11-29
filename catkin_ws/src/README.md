# Mir_SignRecognition
Traffic Sign detection and recognition in Gazebo using YOLO 



# Intallation

```$ cd Mir_SignRecognition/catkin_ws```

```$ cd catkin_make```

# Running the Gazebo worlds

```$ cd Mir_SignRecognition/catkin_ws/src```

```$ source devel/setup.bash```

```$ roslaunch car_demo mcity.launch```

We have provided multiple worlds. The worlds can be fould inside /Mir_signRecognition/catkin_ws/src/car_demo/car_demo/worlds. Load any world for simulation using launch files. 


# Running the Traffic sign recognition

First launch the desired Gazebo simulation environment using,

```$ roslaunch car_demo test_track.launch```

Now, launch the recognition part for loading the neural network, camera images and training weights. 

```$roslaunch darknet_ros recognition.launch```

# Running the Lateral Controller

Lateral controler helps maintain lanes by providing steering angle to the vehicle model. 

``` rosrun lateral_control lateral_controller.py /Mir_signRecognition/Training/weights/lateral_control```

This loades the scripts and weights file necessary for self-driving. 

