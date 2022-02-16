#This standalone code demonstrates the functionality of the limit switches
#implement this in the system-level code at some point
#Hector Juarez
#hjuarez2@nd.edu

#you probably already imported this 
import RPi.GPIO as gpio
import time

#gpio pin should be soldered to NO wire (normally open)
#see https://realpars.com/wp-content/uploads/2020/10/Microswitch-Circuit-Example-1.gif
#common terminal to positive (red)voltage (3.3V)
#NC terminal is (probably) not needed unless you want to detect when the limit is not yet hit
#NO (normally open) terminal is black, this is what will go to GPIO
#also see this https://realpars.com/wp-content/uploads/2020/10/Microswitch-Circuit-Example-1.gif

#output pin gpio17 is the signal pin for this example, change this to whatever you solder it to
#pull_up_down parameter assumes the default state is 0V, change to PUD_UP if it isnt
#https://raspberrypi.stackexchange.com/questions/27263/change-the-gpio-pull-up-down-gpio-pud-up-to-gpio-pud-down

gpio.setup(1, gpio.IN, pull_up_down=GPIO.PUD_DOWN)

while(True):
    if gpio.input(17)==0:
        print("limit switch actuated"+gpio.input(17))
    else:
        print("limit switch not actuated"+gpio.input(17))
    time.sleep(1)