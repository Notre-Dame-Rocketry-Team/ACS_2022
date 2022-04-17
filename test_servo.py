import time
import sys
from adafruit_servokit import ServoKit

#i2c = busio.I2C(board.SCL, board.SDA)
#pca = adafruit_pca9685.PCA9685(i2c)
#pca.frequency = float(sys.argv[2]
CONTROLLER_PIN = 7
STOP = 0.15
kit = ServoKit(channels=16)
servo = kit.continuous_servo[CONTROLLER_PIN]



servo.throttle = float(sys.argv[1])

