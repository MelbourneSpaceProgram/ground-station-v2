from os import read
import time
import board
import busio
from BatCurvInterp import BatCurvInterp
import numpy as np
import RPi.GPIO as GPIO
import subprocess

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS object
ads = ADS.ADS1115(i2c)

# Create a differential channel on Pin 0 and Pin 1 for 1st cell
chan_1 = AnalogIn(ads, ADS.P0, ADS.P1)
# Create a differential channel on Pin 1 and Pin 2 for 2nd cell
chan_2 = AnalogIn(ads, ADS.P1, ADS.P3)

#Create Battery Charge Curve Interpolator (converts current voltage to percentage charge remaining in specific cell)
btinterp = BatCurvInterp(8) #8 represents the order of polynomial (8 was identified as the best during testing)

# Choose frequency of readings per second
READING_FREQ = 2
READING_DELAY = 1/READING_FREQ

#         ADS1115 gain
#       GAIN    RANGE (V)
#          1    +/- 4.096
gain = 1
ads.gain = gain


# Set LED Pins
GPIO.setmode(GPIO.BCM)
RED_LED = 17
YELLOW_LED = 27
GREEN_LED = 22

# Set Off Button
OFF_BUTTON = 10

#Set Critical Battery Voltage
CRITIC_VOLT = 6.7 

#function to safely switch off raspberry pi
def turn_off_rpi():
    """ Use any of the below commands to turn off rpi from terminal
    $ sudo halt
    $ sudo poweroff
    $ sudo shutdown -h now
    $ sudo shutdown -h 10 #Shutdown in 10 mintues
    $ sudo init 0"""
    shut_down()
    pass

# modular function to restart Pi TAKEN FROM https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button/all
def restart():
    print("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# modular function to shutdown Pi TAKEN FROM https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button/all
#command variable has to be redefined to where the sbin is?
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

#Use the current voltage of both batteries, find their respective remaining power level and return the average
def find_power_percent(v1, v2):
    current_charge = np.mean(btinterp.interp_val([v1, v2], True))
    return current_charge

#Choose which led to light based on voltage level
def light_led(v):
    if v > 8.4:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.LOW)
    elif v > 6.9:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
    else:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)

#Initialize all inputs/outputs and interrupts
def start():
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(YELLOW_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(OFF_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(OFF_BUTTON, GPIO.FALLING, callback=turn_off_rpi, bouncetime=100)

    loop()
    
#Continuous loop for script to follow during on time
def loop():
    while True:
        v1 = chan_1.voltage #Cell 1
        v2 = chan_2.voltage #Cell 2
        v_t = v1 + v2 #Combined Total Voltage
        print(f"Current voltage of 2 cell battery pack is: {v_t}")
        print(f"{find_power_percent(v1,v2)}\% power remaining")
        light_led(v_t)
        time.sleep(READING_DELAY) #Could be good idea to do multithreading to run all processes simultaniously


if __name__ == '__main__':
    start()
