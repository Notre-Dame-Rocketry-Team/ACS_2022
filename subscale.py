# Import libraries
import sensors
import logging

# Constants
SAVE_PATH = './data/'
SAVE_NAME = 'data'
SAVE_SUFFIX = '.csv'

def find_new_name():
    './data/data_0.csv'
    './data/data_1.csv'
    './data/data_2.csv'

    # Step 1: search for file names using glob

    # Step 2: if there are any file names, find the biggest number

    # Step 3: find new file name
    pass

def initialize_sensors():
    pass

def read_sensors():
    pass


if __name__ == '__main__':
    # Initialize sensors
    initialize_sensors()

    # Initialize CSV
    logging.initialize_csv()

    while True:
        # Read sensors
        read_sensors()
        
        # Write to CSV
        logging.write_csv()
