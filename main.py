from rpi import snowboydecoder
import sys
import signal
import RPi.GPIO as GPIO
import time
import random
import csv

#read settings file 
settingsReader = csv.reader( open('userdata/settings.csv', "rb"), delimiter=' ')
for row in settingsReader:
    Sbase = row[0]
    drive_s = row[1]
    simple = row[2]


pi = 2*1.30
# pin per rasby
leftWheels = 15
rightWheels = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup( (leftWheels, rightWheels), GPIO.OUT)
#Our relays-board use an inverted logic: low signal trigger the relay.
#This explains why at first look the code can look "weird"
def straight():
    GPIO.output( (leftWheels, rightWheels), False )

def stop():
    GPIO.output( (leftWheels, rightWheels), True )
#To TURN LEFT use right wheels to gain the boost needed
def leftFor( timeInSeconds ):
    stop()
    GPIO.output( rightWheels, False )
    time.sleep( timeInSeconds )
    GPIO.output( (leftWheels, rightWheels), True )
    straight()
#To TURN RIGHT use right wheels to gain the boost needed
def rightFor( timeInSeconds ):
    stop()
    GPIO.output( leftWheels, False )
    time.sleep( timeInSeconds )
    GPIO.output( (leftWheels, rightWheels), True )
    straight()
# Demo code for listening two hotwords at the same time
#___________________________________________________________________________

interrupted = False
angles = [pi/12, pi/6, pi/3]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    stop()
    return interrupted

def alt():
    print("alt")
    stop()

def left(i):
    print('left'+str(i))
    leftFor( angles[i] )

def right(i):
    print('right'+str(i))
    rightFor( angles[i] )

stop()
models = [
          #'models/start.pmdl', 
          'userdata/right1.pmdl', 
          'userdata/right2.pmdl', 
          'userdata/right3.pmdl', 
          'userdata/left1.pmdl', 
          'userdata/left2.pmdl',
          'userdata/left3.pmdl', 
          'userdata/stop.pmdl'
          ]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [
            #start,
            right(1),
            right(2),
            right(3),
            left(1),
            left(2), 
            left(3), 
            alt]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
