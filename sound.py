import RPi.GPIO as GPIO
import subprocess
import time
from os import listdir

'''
CONSTANTS
'''

# Directory where all the sounds we play can be found
SOUNDS_DIR = "/home/pi/rasp-sound-machine/sounds"

# Name of the app used to play the sound
SOUND_ARGS = ["aplay"]

# The GPIO PIN we're listening to
GPIO_PIN = 4

'''
INITIAL SETUP
'''

# Configure GPIO PIN for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Get an array of all the sound files
files = listdir(SOUNDS_DIR)    

# Get the total number of files
totalFiles = len(files)

# Keeps track of what file in the list we're playing
curFilePos = 0

# Keeps track of the PID for the currently playing sound
curPID = 0

'''
TODO: When a button is pressed, do the following:
Play a sound for 20 minutes
If a sound is already playing, play another sound
If at end of sound list, stop playing
'''

'''
LOOP, WAITING FOR BUTTON PRESS
'''
while True:
    input_state = GPIO.input(GPIO_PIN)
    if input_state == False:
        print("Button Pressed")

        # If this is the last file, kill the sound, reset our count and restart the loop
        if curFilePos == totalFiles:
            print("Killing sound and stopping playback")
            curPID.kill()
            curFilePos = 0
            
            # Sleep to ensure button isn't clicked too quickly
            time.sleep(.5)
            continue

        # Kill the old sound if it's playing
        if curPID != 0:
            curPID.kill()
        
        # Spawn a child process to play button
        print("Playing sound %s" % files[curFilePos])
        args = list(SOUND_ARGS)
        args.append(SOUNDS_DIR + "/" + files[curFilePos])
        curPID = subprocess.Popen(args)

        # Print out PID
        print("PID: %d" % curPID.pid)

        # Increment the current file position
        curFilePos += 1

        # Sleep to ensure button isn't clicked too quickly
        time.sleep(.5)

