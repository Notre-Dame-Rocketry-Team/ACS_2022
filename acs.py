"""
This file contains the main code, which will
continually read data from sensors, filter it, 
and write output. It will also call functions to
change the current vehicle state and acs state.
Author: Daniel Noronha
With contributions from Patrick Faley and Hector Juarez
"""

FAKE_DATA = False
FAKE_DATA_SAMPLE_RATE = 10 #Hz
fake_path = 'data_subscale_11_20_launch1.csv'

# Import libraries
import time
import traceback
import data_filter
import scribe
# import sensors
import state
import acs_states
import beep
from data_manager import Data_Manager

# Constants
SAVE_PATH = './data/'
SAVE_NAME = 'data'
SAVE_SUFFIX = '.csv'
MAX_OLD_STATE = 3 # How many times should the same state be reported consequtively before ACS state is updated accordingly?

if __name__ == '__main__':
    # Define Active Sensors
    active_sensors = ['IMU', 'Altimeter']#, 'Accelerometer']
    # Get filename and Create csv file (pointer)
    save_fname = scribe.find_new_name(SAVE_PATH, SAVE_NAME, SAVE_SUFFIX)
    file_p = open(save_fname, 'w', newline='')
    # Initialize CSV
    scribe.newCSV(file_p, manager.get_field_names()) # Write Headers
    # Initialize the Buzzer
    beep.init()
    # Initialize Data Manager
    manager = Data_Manager(active_sensors)
    # Initialize Sensors
    # Check if using Fake Data
    if FAKE_DATA:
        import sensors_spoof as sensors
        sensors.initialize_sensors(fake_path, manager)
    else:
        import sensors
        sensors.initialize_sensors(manager)
    # Initialize Kalman Filter
    data_filter.initialize_filter(manager)
    # Initialize the Launch Vehicle state (OnGround)
    state.init_state(manager)
    # Initialize the ACS State (ACS_OnGround)
    acs_states.init_acs_state(manager)

    beep.beep(2000,2) # One *beep* to verify that the code is running and all initializations are complete!

    # VARIABLES
    count = 0
    current_state_lst = []

    while True:
        try:
            print('--- Beginning Cycle ---')
            # Read sensors (unfiltered)
            t1 = time.time()
            # data = sensors.read_sensors(sensors)
            sensors.read_sensors(manager)
            count += 1#
            print(f"Cycle Count: {count}")
            t2 = time.time()
            print(f'Total Sensor Read Time: {t2 - t1}s')

            # Filter data
            t1 = time.time()
            data_filter.filter_data(manager)
            t2 = time.time()
            print(f'Total Data Filtering Time: {t2 - t1}s')

            # Update Current Launch Vehicle State
            t1 = time.time()
            current_state = state.state_transition(manager)
            t2 = time.time()
            print(f'Launch Vehicle State Update Time: {t2 - t1}s')

            # Update ACS State
            t1 = time.time()
            if len(current_state_lst) < MAX_OLD_STATE:
                current_state_lst.append(current_state)
            else:
                current_state_lst = []
                current_state_lst.append(current_state)
                # If OnGround
            if  (len(current_state_lst) == MAX_OLD_STATE):
                if (current_state == state.states[0]):
                    acs_states.acs_inactive(manager) # ACS Inactive
                # If PoweredAscent (reported 3 times consequtively)
                elif (current_state == state.states[1]) and (all(i == current_state_lst[0] for i in current_state_lst)):
                    acs_states.acs_armed(manager) # ACS Armed
                # If Burnout (reported 3 times consequtively)
                elif (current_state == state.states[2]) and (all(i == current_state_lst[0] for i in current_state_lst)):
                    acs_states.acs_active(manager) # ACS Active
                # If Overshoot (reported 3 times consequtively)
                elif (current_state == state.states[3]) and (all(i == current_state_lst[0] for i in current_state_lst)):
                    acs_states.acs_active_MAX(manager) # ACS Active MAX
                # If Apogee
                elif (current_state == state.states[-1]):
                    acs_states.acs_inactive(manager) # ACS Inactive

            else:
                manager.update_field('ACS_state',acs_states.acs_state)
            t2 = time.time()
            print(f'ACS State Update Time: {t2 - t1}s')

            # Write/Log to CSV
            t1 = time.time()
            scribe.addRow(file_p, manager.get_field_values())
            t2 = time.time()
            print(f'Data Write Time: {t2 - t1}s')
            print()
            if FAKE_DATA:
                time.sleep(1/FAKE_DATA_SAMPLE_RATE)
        # Error Handling
        except Exception:
            print('Sorry, this program is experiencing a glitch :-(')
            print(traceback.format_exc())
            with open('log.txt','w') as err_log:
                err_log.write(traceback.format_exc())
            acs_states.acs_FAILURE(manager)
            file_p.close()
            for beeps in range(1,10):
                beep.beep(440,1) # ERROR *BEEPS*
                time.sleep(0.5)
            break

