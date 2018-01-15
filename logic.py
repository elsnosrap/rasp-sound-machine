import subprocess
import time
from os import listdir
import threading

# This file is used to implement the logic in sound.py only
# on any other machine than a raspberry pi

# Directory where all the sounds we play can be found
SOUNDS_DIR = "/Users/tparsons/dev/git/rasp-sound-machine/short-sounds"

# Name of the app used to play the sound
SOUND_ARGS = ["sox-macosx/play", "-q", "-V 0"]

# The number of seconds to play a sound for
SECONDS_TO_PLAY = 10

'''
INITIAL SETUP
'''

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
# Our method that plays back a sound in a separate thread
def playback(audioFile):
    args = list(SOUND_ARGS)
    args.append(audioFile)
    global curPID

    # Make note of when playback started
    startTime = time.time()
    print("Start time: %d" % startTime)

    while True:
        # Start playback
        curPID = subprocess.Popen(args)
        print("PID: %d" % curPID.pid)

        # Wait for sound to finish playing
        curPID.wait()

        # Check if we should start playback, or stop
        curTime = time.time()
        print('Current time: {}'.format(curTime))
        print('startTime + SECONDS_TO_PLAY: {}'.format(startTime + SECONDS_TO_PLAY))
        if curTime > startTime + SECONDS_TO_PLAY:
            print("We've played enough, we're done here")
            break;
        else:
            print("Haven't played enough, continue")
            continue;

'''
LOOP, WAITING FOR BUTTON PRESS
'''
while True:
    # Emulate our button on the Raspberry pi
    text = input("Press a button")

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
    
    # Play back audio in a separate thread
    playThread = threading.Thread(target=playback, args=(SOUNDS_DIR + "/" + files[curFilePos],))
    playThread.start()

    # Increment the current file position
    curFilePos += 1

    # Sleep to ensure button isn't clicked too quickly
    time.sleep(.5)

