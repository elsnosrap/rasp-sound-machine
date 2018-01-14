import RPi.GPIO as GPIO
import subprocess
import time

# The GPIO PIN we're listening to
GPIO_PIN = 4

# Configure GPIO PIN for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Continuosly loop, listening for input from GPIO
while True:
    input_state = GPIO.input(GPIO_PIN)
    if input_state == False:
        print("Button Pressed")
        
        # Spawn a child process to play button
        pid = subprocess.Popen(["aplay", "/home/pi/Downloads/beach.wav"])

        # Print out PID
        print("PID: %d" % pid.pid)

        # sleep for 500ms to ensure button isn't clicked too quickly
        time.sleep(.5)

        print("Awaiting another button press")

'''
TODO: When a button is pressed, do the following:
Play a sound for 20 minutes
If a sound is already playing, play another sound
If at end of sound list, stop playing
'''
