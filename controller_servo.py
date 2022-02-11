'''
This program contains functions to initialize the servo controller (PCA9685), 
the servo, and to actuate the servo motor.
'''

# RUN sudo pip3 install adafruit-circuitpython-pca9685
# RUN sudo pip3 install adafruit-circuitpython-servokit

# Imports
import time
from adafruit_servokit import ServoKit
import data_manager
from data_manager import Data_Manager
import RPi.GPIO as GPIO

# CONSTANTS
CONTROLLER_PIN = 5

# Global Constants defined in functions
kit = None
servo = None

def init_controller():
    '''
    This function initializes the PCA 9685 controller
    '''
    global kit
    kit = ServoKit(channels=16)
    GPIO.setmode(GPIO.BCM) # Initialize GPIO
    GPIO.setup(23, GPIO.OUT, initial=1)
    return True

def init_servo():# manager: Data_Manager
    '''
    This function initializes the Continuous rotation servo
    '''
    # Continuous Rotation Servo
    global servo
    servo = kit.continuous_servo[CONTROLLER_PIN]
    #manager.add_data(data_manager.Scalar_Data('servo_Throttle'))
    return True

def servo_throttle(throttle):#manager: Data_Manager
    '''
    This function allows the user to change the servo rotation speed.
    It is a continuous rotation servo.
    For full throttle: throttle = 1
    For zero throttle(stop): throttle = 0
    For full reverse throttle: throttle = -1
    Enter a decimal value to control speeds inbetween -1 and 1.
    '''
    servo.throttle = throttle
    #manager.update_field('servo_Throttle', throttle)
    print(f"Servo Throttle: {throttle} = {throttle * 100}%") # Only for testing
    return throttle

# TESTING
try:
    init_controller()
    init_servo()
    while True:
<<<<<<< HEAD
        GPIO.output(23, 0)
        servo_throttle(1)
        time.sleep(5)
        servo_throttle(-1)
        time.sleep(5)
=======
#servo_throttle(1)
#time.sleep(5)
#servo_throttle(-1)
#time.sleep(5)
        servo_throttle(0)
>>>>>>> 3a8662592ea61b559688d7a989ca7459f122f71d
except KeyboardInterrupt:
    GPIO.output(23, 0)
    servo_throttle(0)
    servo_throttle(0)
    servo_throttle(0)


