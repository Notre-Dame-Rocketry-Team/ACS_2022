'''
This program contains functions to initialize the servo controller (PCA9685), 
the servo, and to actuate the servo motor.
'''


# Imports
import time
from tkinter.tix import MAX
from adafruit_servokit import ServoKit
import data_manager
from data_manager import Data_Manager
import RPi.GPIO as gpio
# Initialize the Limit Switches
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(27, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# CONSTANTS
CONTROLLER_PIN = 5
STOP = 0.15 # Use this for servo.throttle() to stop the motor
MAX_UP = -1
MAX_DOWN = 1

# Global Constants defined in functions
kit = None
servo = None

def init_controller():
    '''
    This function initializes the PCA 9685 controller
    '''
    global kit
    kit = ServoKit(channels=16)
    return True

def init_servo(manager: Data_Manager):
    '''
    This function initializes the Continuous rotation servo
    '''
    # Continuous Rotation Servo
    global servo
    servo = kit.continuous_servo[CONTROLLER_PIN]
    servo.throttle = STOP
    manager.add_data(data_manager.Scalar_Data('servo_Throttle'))
    return True

def servo_throttle(throttle, manager: Data_Manager):
    '''
    This function allows the user to change the servo rotation speed.
    It is a continuous rotation servo.
    To move up: throttle = -1
    For zero throttle(STOP): throttle = 0.15
    To move down: throttle = 1
    Enter a decimal value to control speeds inbetween -1 and 1.
    '''
    servo.throttle = throttle
    manager.update_field('servo_Throttle', throttle)
    #print(f"Servo Throttle: {throttle} = {throttle * 100}%") # Only for testing
    return throttle

def servo_up(manager: Data_Manager):
    return servo_throttle(MAX_UP,manager)

def servo_down(manager: Data_Manager):
    return servo_throttle(MAX_DOWN,manager)

def servo_stop(manager: Data_Manager):
    return servo_throttle(STOP,manager)


# TESTING
'''
init_controller()
init_servo()
while True:
    #servo_throttle(-1)
    #time.sleep(5)
    servo_throttle(1)
    time.sleep(7)
    servo_throttle(STOP)
    time.sleep(5)
        #GPIO.output(23,1)
'''
