import sys
import time
MPU_PATH = '/home/pi/repos/micropython-mpu9250-master'
sys.path.append(MPU_PATH)
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)

print("MPU9250 id: " + hex(sensor.whoami))

while True:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.magnetic)
    print(sensor.temperature)

    time.sleep_ms(1000)
