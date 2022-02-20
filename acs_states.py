'''
Author: Daniel Noronha
With contributions from Hector Juarez
This program defines the possible
ACS States as part of the control algorithm.
'''
# Imports
import time
import controller_servo
# import PID_control
import data_manager
from data_manager import Data_Manager

UPPER_LIMIT_SWITCH_PIN = 17
LOWER_LIMIT_SWITCH_PIN = 27

acs_states = [
    'ACS_Inactive',
    'ACS_Armed',
    'ACS_Active',
    'ACS_Active_MAX',
    'ACS_Failure'
]
acs_state = ''
acs_timer_start = None
sw_timer_start = None

# ACS Functions
def init_acs_state(manager: Data_Manager) -> bool:
    '''
    This function adds 'ACS_state' to the data manager for logging purposes.
    '''
    controller_servo.init_controller()
    controller_servo.init_servo(manager)
    controller_servo.servo_stop(manager)
    global acs_timer_start
    global acs_state
    acs_timer_start = None
    # Add ACS_state to manager for logging purposes
    manager.add_data(data_manager.Scalar_Data('ACS_state'))
    # Initialize the flap position so that flaps are fully retracted
    while controller_servo.gpio.input(LOWER_LIMIT_SWITCH_PIN) == 0:
        if int(controller_servo.servo.throttle) != controller_servo.MAX_DOWN:
            controller_servo.servo_down(manager)
        else:
            continue
    controller_servo.servo_up(manager)
    time.sleep(1)
    controller_servo.servo_stop(manager)
    
    acs_state = acs_states[0] # ACS_Inactive
    return True

def acs_inactive(manager: Data_Manager):
    '''
    This function applies HIGH voltage to OE pin to disable servo outputs when ACS is inactive.
    '''
    global acs_state
    global inactive_second_time
    acs_state = acs_states[0]
    if int(controller_servo.servo.throttle) != int(controller_servo.STOP):
        controller_servo.servo_throttle(controller_servo.STOP, manager)
    else:
        manager.update_field('servo_Throttle', controller_servo.servo.throttle)
    if inactive_second_time:
        init_acs_state(manager)
    manager.update_field('ACS_state',acs_state)


def acs_armed(manager: Data_Manager):
    '''
    This function performs actions necessary to arm the ACS system
    '''
    global acs_state
    acs_state = acs_states[1] # ACS_Armed
    if int(controller_servo.servo.throttle) != int(controller_servo.STOP):
        controller_servo.servo_throttle(controller_servo.STOP, manager)
    else:
        manager.update_field('servo_Throttle', controller_servo.servo.throttle)
    manager.update_field('ACS_state',acs_state)

def acs_active(manager: Data_Manager):
    '''
    This function calls the PID control algorithm to actuate the servo
    '''
    # Call PID_control functions here as required
    # controller_servo.servo_throttle(controller_servo.MAX_UP, manager)
    global acs_timer_start
    global acs_state
    global sw_timer_start
    
    #modified initial movement for testing
    if (sw_timer_start == None) and (controller_servo.gpio.input(LOWER_LIMIT_SWITCH_PIN) == 1):
        sw_timer_start = time.time()
        controller_servo.servo_up(manager)
    elif (sw_timer_start == None) and (controller_servo.gpio.input(UPPER_LIMIT_SWITCH_PIN) == 1):
        sw_timer_start = time.time()
        controller_servo.servo_down(manager)
    elif (sw_timer_start != None) and (time.time() - sw_timer_start >= 1):
        controller_servo.servo_stop(manager)
        # sw_timer_start = None**
    elif (acs_timer_start == None) and (sw_timer_start == None):
        acs_timer_start = time.time()
        controller_servo.servo_up(manager)

    elif (time.time()-acs_timer_start >= 10) and (sw_timer_start == None): # and (int(controller_servo.servo.throttle) == controller_servo.MAX_UP))**
        controller_servo.servo_down(manager)
    else:
        manager.update_field('servo_Throttle', controller_servo.servo.throttle)
        

    acs_state = acs_states[2] # ACS_Active
    manager.update_field('ACS_state',acs_state)

def acs_active_MAX(manager: Data_Manager):
    '''
    This function bypasses the PID control algorithm to actuate the servo to its Maximum value
    '''
    # Call required controller_servo function (100% actuation) directly here
    # controller_servo.servo_throttle(controller_servo.MAX_UP, manager)
    global acs_state
    acs_state = acs_state[3] # ACS_Active_MAX
    controller_servo.servo_stop(manager)
    manager.update_field('ACS_state',acs_state)

def acs_FAILURE(manager: Data_Manager):
    '''
    This function is a failure mode. It only activates in case of a fatal error (and logs the same).
    '''
    global acs_state
    # controller_servo.servo_throttle(controller_servo.STOP, manager)
    acs_state = acs_state[-1] # ACS_Failure mode
    manager.update_field('ACS_state',acs_state)
