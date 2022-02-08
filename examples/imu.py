"""
This is an example of a data collection Python script for the ICM-20948 IMU.
Wiring and CircuitPython/Python setup information can be found at:
https://learn.adafruit.com/adafruit-tdk-invensense-icm-20948-9-dof-imu/python-circuitpython
"""

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_icm20x

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
print(icm.acceleration)
print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
print("")

