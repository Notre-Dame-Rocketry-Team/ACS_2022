#This standalone code demonstrates the functionality of the limit switches
#implement this in the system-level code at some point
#Hector Juarez
#hjuarez2@nd.edu

#you probably already imported this 
import RPi.GPIO as gpio
import time

#postive and negative can (probably) take 5V


#output pin 21 is the signal pin for this example, change this to whatever you solder it to
#pull_up_down parameter assumes the default state is 0V, change to PUD_down if it isnt
gpio.setup(21, gpio.IN, pull_up_down=GPIO.PUD_UP)


while(True)
    if gpio.input(21)==0:
        print "limit switch actuated"
    else:
        print "limit switch not actuated"
    time.sleep(1)