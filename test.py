import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # Initialize GPIO
GPIO.setup(23, GPIO.OUT, initial=0) # Set OE pin on controller to LOW initially (enables all outputs)
GPIO.output(23, 0) # Enables all outputs (Pin: LOW)
CONTROLLER_PIN = 5
kit = ServoKit(channels=16)
try:
    while True:
        GPIO.output(23, 0)
        kit.continuous_servo[CONTROLLER_PIN].throttle = -0.8
        print(f"Servo Throttle: {kit.continuous_servo[CONTROLLER_PIN].throttle} = {kit.continuous_servo[CONTROLLER_PIN].throttle * 100}%")
        time.sleep(1)
except KeyboardInterrupt:
    kit.continuous_servo[CONTROLLER_PIN].throttle = 0
    kit.continuous_servo[CONTROLLER_PIN].throttle = 0
    kit.continuous_servo[CONTROLLER_PIN].throttle = 0
    #print(f"Servo Throttle: {servo.throttle} = {servo.throttle * 100}%")
    pass


