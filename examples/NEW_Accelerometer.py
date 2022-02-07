"""

New Accelerometer code

Basically a copy of the previous code, but for the DFROBOT H3LIS200DL sensor we stole from Payload

Based on https://github.com/DFRobot/DFRobot_LIS/blob/master/python/raspberrypi/examples/H3LIS200DL/get_acceleration/get_acceleration.py

NDRT ACS 2021-2022
Hector Juarez
hjuarez2@nd.edu

"""

import sys
LIS_PATH = '/home/pi/repos/DFRobot_LIS/python/raspberrypi'
sys.path.append(LIS_PATH)

from DFRobot_LIS import *
import time

I2C_BUS         = 0x01            #default use I2C1
ADDRESS_1       = 0x19            #Sensor address 1
acce = DFRobot_H3LIS200DL_I2C(I2C_BUS ,ADDRESS_1)


#Chip initialization
acce.begin()
#Get chip id
print('chip id :%x'%acce.get_id())

#set range to +-100g
#alternatively change to acce.H3LIS200DL_200G for +-200g, but we probs don't need this
acce.set_range(acce.H3LIS200DL_100G)

#set sample rate and wait for changes to apply
acce.set_acquire_rate(acce.NORMAL_400HZ)
time.sleep(0.1)

while True:
    #Get the acceleration in the three directions of xyz one time 
    x,y,z = acce.read_acce_xyz()
    print("Acceleration [X = %.3f g,Y = %.3f g,Z = %.3f g]"%(x,y,z))
    time.sleep(1)
    
