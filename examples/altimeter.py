"""
This is an example of how to use the BMP390 altimeter. Full wiring
steps can be found at:

Guide: https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx/python-circuitpython
GitHub: https://github.com/adafruit/Adafruit_BMP3XX
"""

# Import libraries
import time
import board
import adafruit_bmp3xx

# Initialize sensor
i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# Get pressure/temperature readings
print("Pressure: {:6.1f}".format(bmp.pressure))
print("Temperature: {:5.2f}".format(bmp.temperature))

# Initialize altitude and get reading
bmp.sea_level_pressure = 1013.25
print('Altitude: {} meters'.format(bmp.altitude))
