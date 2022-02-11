'''
Author: Daniel Noronha
This program defines the possible
ACS States as part of the control algorithm.
'''
# Imports
import controller_servo
# import PID_control
import data_manager
from data_manager import Data_Manager

acs_states = [
    'ACS_Inactive',
    'ACS_Armed',
    'ACS_Active',
    'ACS_Active_MAX',
    'ACS_Failure'
]
acs_state = ''
# ACS Functions
def init_acs_state(manager: Data_Manager) -> bool:
    '''
    This function adds 'ACS_state' to the data manager for logging purposes.
    '''
    controller_servo.init_controller()
    controller_servo.init_servo(manager)
    controller_servo.servo_throttle(controller_servo.STOP, manager)
    global acs_state
    # Add ACS_state to manager for logging purposes
    manager.add_data(data_manager.Scalar_Data('ACS_state'))
    acs_state = acs_states[0] # ACS_Inactive
    return True

def acs_inactive(manager: Data_Manager):
    '''
    This function applies HIGH voltage to OE pin to disable servo outputs when ACS is inactive.
    '''
    global acs_state
    acs_state = acs_states[0]
    controller_servo.servo_throttle(controller_servo.STOP, manager)
    manager.update_field('ACS_state',acs_state)


def acs_armed(manager: Data_Manager):
    '''
    This function performs actions necessary to arm the ACS system
    '''
    global acs_state
    acs_state = acs_states[1] # ACS_Armed
    controller_servo.servo_throttle(controller_servo.STOP, manager)
    manager.update_field('ACS_state',acs_state)

def acs_active(manager: Data_Manager):
    '''
    This function calls the PID control algorithm to actuate the servo
    '''
    # Call PID_control functions here as required
    # controller_servo.servo_throttle(controller_servo.MAX_UP, manager)
    global acs_state
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
    manager.update_field('ACS_state',acs_state)

def acs_FAILURE(manager: Data_Manager):
    '''
    This function is a failure mode. It only activates in case of a fatal error (and logs the same).
    '''
    global acs_state
    # controller_servo.servo_throttle(controller_servo.STOP, manager)
    acs_state = acs_state[-1] # ACS_Failure mode
    manager.update_field('ACS_state',acs_state)
