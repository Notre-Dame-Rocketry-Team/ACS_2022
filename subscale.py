# Import libraries
import sensors
import logging
import glob

# Constants
SAVE_PATH = './data/'
SAVE_NAME = 'data'
SAVE_SUFFIX = '.csv'

def find_new_name():
    './data/data_0.csv'
    './data/data_1.csv'
    './data/data_2.csv'
    './data/data_3.csv'
    './data/data_4.csv'
    './data/data_5.csv'
    './data/data_6.csv'
    './data/data_7.csv'
    './data/data_8.csv'
    './data/data_9.csv'
    './data/data_10.csv'
    # Step 1: search for file names using glob
    files = glob.glob(SAVE_PATH + SAVE_NAME + "_*" + SAVE_SUFFIX)

    # Step 2: if there are any file names, find the biggest number
    numbers= []

    for x in files: 
        y=x.replace(SAVE_PATH + SAVE_NAME + "_", "").replace(SAVE_SUFFIX, "")
        int(y)
        y=int(y)
        numbers.append(y)
    z=max(numbers)
    a=(SAVE_PATH + SAVE_NAME + "_"+z + SAVE_SUFFIX)
    return a
        
    
    # Step 3: find new file name
    import glob
        glob.glob('./data/data_(*-1).csv')
        return: max

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
