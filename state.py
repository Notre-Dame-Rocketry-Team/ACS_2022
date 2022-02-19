'''
Author: Daniel Noronha
This program determines the current state
of the launch vehicle using Kalman-filtered data.
'''
# Import Libraries
import time
import data_manager
from data_manager import Data_Manager

# State Value Constants
states = [
    'OnGround',
    'PoweredAscent',
    'Burnout',
    'Overshoot',
    'Apogee'
]
state = ''
# Sensor State Constants
LAUNCH_ACCEL = 20 # m/s^2
LAUNCH_ALT = 60 # m
BURNOUT_ACCEL = -6.125 # m/s^2
# BURNOUT_ALT = 300 # m
APOGEE_VELOCITY = 0 # m/s
APOGEE_ALT = 1463 # m (4800ft)
CYCLE_DELAY = 300 # s (5 minutes) # Approx. how long will it take to reach the ground after apogee?

# Functions
def init_state(manager: Data_Manager):
    '''
    This function adds 'State' to the data manager for logging purposes.
    The launch vehicle state is also defaulted to OnGround.
    '''
    global state
    manager.add_data(data_manager.Scalar_Data('State'))
    state = states[0] # Default state: OnGround
    return True

def state_transition(manager: Data_Manager):
    '''
    This function updates (data manager) and returns (to caller) the current launch vehicle state.
    It uses altitude, acceleration, and velocity from the Kalman filter.
    '''
    global state
    t_apogee = None # This declaration is not required (only included to suppress syntax error highlighting).
    # Read in data from manager
    altitude = manager.read_field('Kalman_altitude').get_value()
    velocity = manager.read_field('Kalman_velocity').get_value()
    acceleration = manager.read_field('Kalman_acceleration').get_value()
    # OnGround state => PoweredAscent state
    if (state == states[0]) and ((altitude >= LAUNCH_ALT) and (acceleration >= LAUNCH_ACCEL)):
        next_state = states[1]
    # PoweredAscent state => Burnout state
    elif (state == states[1]) and ((altitude < APOGEE_ALT) and (acceleration <= BURNOUT_ACCEL)): # No chance of burnout AFTER desired apogee right?
        next_state = states[2]
    # Burnout state => Overshoot state (Option 1)
    elif (state == states[2]) and ((altitude > APOGEE_ALT) and (acceleration < BURNOUT_ACCEL)):
        next_state = states[3]
    # Burnout state => Apogee state (Option 2) - no overshooting
    elif (state == states[2]) and ((altitude <= APOGEE_ALT) and (velocity < APOGEE_VELOCITY)):
        next_state = states[-1]
        t_apogee = time.time()
    # Overshoot state => Apogee state
    elif (state == states[3]) and ((altitude > APOGEE_ALT) and (velocity < APOGEE_VELOCITY)):
        next_state = states[-1]
        t_apogee = time.time()
    # Apogee state => OnGround state (after remaining in Apogee state for CYCLE_DELAY minutes)
    elif (state == states[-1]) and ((time.time() - t_apogee) > CYCLE_DELAY):
        next_state = state[0]
    else:
    # If no condition is met, remain in the current state (so we can loop and try again)
        next_state = state

    state = next_state
    # Record result (log in data manager)
    manager.update_field('State', state)
    return state

