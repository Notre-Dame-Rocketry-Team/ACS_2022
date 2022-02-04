"""
This file contains the main code, which will
continually read data from sensors, filter it, 
and write output.
Author: Daniel Noronha
Major Contributions from Patrick Faley and other ACS squad members
"""
# Import libraries
import time
import traceback
import data_filter
import scribe
import sensors
import beep
from data_manager import Data_Manager

# Constants
SAVE_PATH = './data/'
SAVE_NAME = 'data'
SAVE_SUFFIX = '.csv'

# piezo = beep.buzzer()

if __name__ == '__main__':
    # Initialize sensors
    # sensors, labels = initialize_sensors()
    # Define Active Sensors
    active_sensors = ['IMU', 'Accelerometer', 'Altimeter']
    # Initialize Data Manager
    manager = Data_Manager(active_sensors)
    # Initialize Sensors
    sensors.initialize_sensors(manager)
    # Initialize Kalman Filter
    data_filter.initialize_filter(manager)
    # Initialize the Buzzer
    beep.init()
    beep.beep(440,2) # One *beep* to verify that the code is running!

    # Get filename and Create csv file (pointer)
    save_fname = scribe.find_new_name(SAVE_PATH, SAVE_NAME, SAVE_SUFFIX)
    f = open(save_fname, 'w', newline='')
    # Initialize CSV
    scribe.newCSV(f, manager.get_field_names()) # Write Headers

    # Initialize CSV


    while True:
        try:
            print('--- Beginning Cycle ---')
            # Read sensors (unfiltered)
            t1 = time.time()
            # data = sensors.read_sensors(sensors)
            sensors.read_sensors(manager)
            t2 = time.time()
            print(f'Total Sensor Read Time: {t2 - t1}')
            # Filter data
            t1 = time.time()
            data_filter.filter_data(manager)
            t2 = time.time()
            print(f'Total Data Filtering Time: {t2 - t1}')
            # Write to CSV
            t1 = time.time()
            scribe.addRow(f, manager.get_field_values())
            t2 = time.time()
            print(f'Data Write Time: {t2 - t1}')
            print()
        # Error Handling
        except Exception:
            print('Sorry, this program is experiencing a glitch :(')
            print(traceback.format_exc())
            f.close()
            for beeps in range(1,10):
                beep.beep(2000,1)
                time.sleep(0.5)


#INIT_FUNCTIONS = [sensors.init_time,
#                  sensors.init_imu,
#                   sensors.init_accelerometer,
#                   sensors.init_altimeter]
# READ_FUNCTIONS = [sensors.read_time,
#                   sensors.read_imu,
#                   sensors.read_accelerometer,
#                   sensors.read_altimeter]

# DEPRECATED - Initialize sensors defined in sensors.py itself
# def initialize_sensors():
#     """
#     This function calls all of the functions specified in
#     INIT_FUNCTIONS to initialize all of the sensors.
#     The output from a function in INIT_FUNCTIONS should
#     be of the following form:

#     Outputs: objects - list of sensor objects
#              labels - list of string labels for sensors
#     """

#     # Run all the functions
#     out = [f() for f in INIT_FUNCTIONS]

#     # Break it apart
#     objects, labels = utils.unzip_list(out)
#     labels = utils.unroll_list(labels)

#     return objects, labels
# DEPRECATED - Read sensors defined in sensors.py itself
# def read_sensors(sensors):
#     """
#     This function calls all of the functions specified in
#     READ_FUNCTIONS to read data from all sensors.
#     The output should be a list of all of the sensor data,
#     in the order of the label output from `initialize_sensors`

#     Inputs: sensors - list of sensor objects
#     Outputs: data - list of floats with sensor data
#     """

#     # Run all the functions
#     data = [f(obj) for f, obj in zip(READ_FUNCTIONS, sensors)]
#     data = utils.unroll_list(data)

#     return data
