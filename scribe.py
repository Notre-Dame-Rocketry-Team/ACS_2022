# NDRT 2021-2022
# Hector Juarez ACS subteam
# Modified by Daniel Noronha ACS subteam (includes function to find a new csv filename)
# This code contains functions to create CSV files and add data to them
#
# Note that each of the following functions opens/closes a csv file every time it is called,
# as well as creates a new csv writer object. Perhaps consider moving these steps outside of the functions
# upon code integration, so that these steps are only done once when the code is run. 

# Also, these two functions are identical, but named differently for ease of use and clarity

import csv
import glob
# finds a new CSV filename
# inputs: SavePath, SaveName, and SaveSuffix
# returns: filename
def find_new_name(SAVE_PATH, SAVE_NAME, SAVE_SUFFIX):
    # Step 1: search for file names using glob
    files = glob.glob(SAVE_PATH + SAVE_NAME + "_*" + SAVE_SUFFIX)

    # Step 2: if there are any file names, find the biggest number
    numbers = []

    for x in files: 
        numbers.append(int(x.replace(SAVE_PATH + SAVE_NAME + "_", "").replace(SAVE_SUFFIX, "")))

    z = 1 + max(numbers) if len(numbers) > 0 else 0

    # Step 3: Return the output file name
    if z < 10:
        fname = SAVE_PATH + SAVE_NAME + '_0' + str(z) + SAVE_SUFFIX
    else:
        fname = SAVE_PATH + SAVE_NAME + '_' + str(z) + SAVE_SUFFIX

    return fname
# creates a new CSV file - modified to use csv.DictWriter() and writeheader() methods to work with Data Manager.
# input: filepath to new CSV file, list of headers as a python list
# returns: n/a
def newCSV(f, headers):
    # open file in write mode
    #with open(filepath, 'w', newline='') as f:
        # create the csv writer
        #writer = csv.writer(f)
    writer = csv.DictWriter(f, fieldnames = headers) # manager.get_field_names()
    # write the headers to the csv file
    #writer.writerow(headers)
    writer.writeheader()

# adds a row of data to a given CSV file
# input: filepath to new CSV file, row of data as a python list
# output: n/a
def addRow(f, row):
    # open file in write mode
    #with open(filepath, 'a', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)
    # write a row to the csv file
    writer.writerow(row)
