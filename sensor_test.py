'''
Test all sensors together
'''

import time
import board
import adafruit_icm20x
#import adafruit_bmp3xx
import sys
LIS_PATH = '/home/pi/repos/DFRobot_LIS/python/raspberrypi'
sys.path.append(LIS_PATH)

from DFRobot_LIS import *
import time

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
print("")
'''#
# Initialize sensor
i2c = board.I2C()
altimeter = adafruit_bmp3xx.BMP3XX_I2C(i2c)
altimeter.pressure_oversampling = 1
altimeter.temperature_oversampling = 1
altimeter.filter_coefficient = 0

# Zero out altimeter
N = 100
sea_sum = 0
for _ in range(N):
    sea_sum += altimeter.pressure
    time.sleep(0.01)
altimeter.sea_level_pressure = sea_sum / N
# Get pressure/temperature readings
print(altimeter.pressure)
print(altimeter.temperature)
print(altimeter.altitude)

'''#
'''#
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

    #Get the acceleration in the three directions of xyz one time 
x,y,z = acce.read_acce_xyz()
print("Acceleration [X = %.3f g,Y = %.3f g,Z = %.3f g]"%(x,y,z))
time.sleep(1)

'''