"""
This file contains all the code used to 
filter the sensor data, with whatever
libraries are required
"""

# Import libraries
import data_manager
from data_manager import Data_Manager
import numpy as np
import matplotlib.pyplot as plt
# import openpyxl
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise


# Global variables
my_filter = None
t_prev = None

g = 9.80665


# Functions
def initialize_filter(manager: Data_Manager):
    """
    This function initializes the Kalman filter and
    returns the initialized filter.
    """

    global my_filter

    # Initialize measurement matrix based on number/type of sensors
    H = []
    if 'Altimeter' in manager.active_sensors:
        H.append([1,0,0])
    if 'Accelerometer' in manager.active_sensors:
        H.append([0,0,1])
    if 'IMU' in manager.active_sensors:
        H.append([0,0,1])

    # Initialize object
    my_filter = KalmanFilter(dim_x=3, dim_z=len(H))       

    # Measurement/state conversion matrix
    my_filter.H = np.array(H)

    # Covariance matrix
    my_filter.P *= 1

    # Measurement Noise
    my_filter.R *= 1

    # Process Noise
    # my_filter.Q = Q_discrete_white_noise(dim=3, dt=0.1, var=0.13)
    my_filter.Q *= 1

    # Initial position
    my_filter.x = np.array([0,0,0])

    # Initialize data manager
    manager.add_data(data_manager.Scalar_Data('kalman_height'))
    manager.add_data(data_manager.Scalar_Data('kalman_velocity'))
    manager.add_data(data_manager.Scalar_Data('kalman_acceleration'))

    
def gen_phi(dt):
    """"
    This function generates a state transition matrix
    "phi" from a timestep.
    """
    dp = 1
    ds = 0
    di = (dt**2)/2

    phi = np.array([[dp, dt, di],
                    [ds, dp, dt],
                    [ds, ds, dp]])

    return phi

def get_dt(in_time):
    """
    Appropriately handle the creation of
    a timestep from the current and previous
    times.
    """
    global t_prev

    if t_prev == None:
        dt = 0.1
    else:
        dt = in_time - t_prev
    t_prev = in_time
    return dt

def transform_adxl(in_accel):
    out_accel = float(in_accel[2])-9.5244
    #print(f'ADXL: {in_accel[2]}, {out_accel}')
    return out_accel

def transform_mpu(in_accel):
    out_accel = g*(float(in_accel[2])-0.53)
    #print(f'MPU: {in_accel[2]}, {out_accel}')
    return out_accel


def filter_data(manager: Data_Manager):
    """
    Author: Patrick
    This is the main function, which 
    filters incoming sensor data
    Input: sensor_data - a dict of data with these fields:
        - accelerometer: ordered tuple
          containing the x, y, and z
          accelerations
        - altimeter: the current height
          of the rocket
        - imu: a dict containing data from the IMU
            - acceleration: ordered tuple containing
              x, y, and z accelerations
            - orientation: ordered tuple containing
              the roll, pitch, and yaw of the rocket
    Output: ordered tuple containing the estimated
    height, (vertical) velocity, acceleration, and angle
    with   the ground
    """

    # Load globals
    global my_filter
    global t_prev

    # Make sure filter is initialized
    if my_filter == None:
        raise Exception("Filter not initialized!")

    # Read in sensor data
    measurements = []
    if 'Altimeter' in manager.active_sensors:
        measurements.append(float(manager.read_field('mpl_altitude').get_value()))
    if 'Accelerometer' in manager.active_sensors:
        accel = manager.read_field('adxl_acceleration').get_value_list()
        measurements.append(transform_adxl(accel))
    if 'IMU' in manager.active_sensors:
        accel = manager.read_field('mpu_acceleration').get_value_list()
        measurements.append(transform_mpu(accel))
            
    t = float(manager.read_field('time').get_value())
    dt = get_dt(t)

    # Appropriately update filter parameters
    z = np.array(measurements)
    my_filter.F = gen_phi(dt)

    # Perform the prediction/update steps
    my_filter.predict()
    my_filter.update(z)

    # Log the output
    y,v,a = my_filter.x
    manager.update_field('kalman_height', y)
    manager.update_field('kalman_velocity', v)
    manager.update_field('kalman_acceleration', a)

    #print(f'Kalman: {a}')
