import time
from adafruit_servokit import ServoKit
CONTROLLER_PIN = 5
kit = ServoKit(channels=16)
servo = kit.continuous_servo[CONTROLLER_PIN]
try:
    while True:
        servo.throttle = -1
        print(f"Servo Throttle: {servo.throttle} = {servo.throttle * 100}%")
except KeyboardInterrupt:
    servo.throttle = 0
    servo.throttle = 0
    servo.throttle = 0
    print(f"Servo Throttle: {servo.throttle} = {servo.throttle * 100}%")


