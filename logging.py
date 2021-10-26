# NDRT 2021-2022
# ACS subteam
# This code contains functions to create CSV files and add data to them 

import csv

# creates a new CSV file
# input: filepath to new CSV file, list of headers as a python list
# returns: n/a
def newCSV(filepath,headers):
    # open file
    with open(filepath, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(headers)

# adds a row of data to a given CSV file
# input: filepath to new CSV file, row of data as a python list
# output: n/a
def addRow(filepath,row):
    # open file
    with open(filepath, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(headers)