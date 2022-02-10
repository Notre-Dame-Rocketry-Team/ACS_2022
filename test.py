import time
from adafruit_servokit import ServoKit
CONTROLLER_PIN = 5
kit = ServoKit(channels=16)
try:
    while True:
        kit.continuous_servo[5].throttle = -0.8
        #print(f"Servo Throttle: {servo.throttle} = {servo.throttle * 100}%")
        time.sleep(1)
except KeyboardInterrupt:
    #servo.throttle = 0
    #servo.throttle = 0
    #servo.throttle = 0
    #print(f"Servo Throttle: {servo.throttle} = {servo.throttle * 100}%")
    pass


