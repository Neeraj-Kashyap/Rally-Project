from rpi import snowboydecoder
import sys
import signal
import RPi.GPIO as GPIO
import time
import random
import csv

#read settings file 
settingsReader = csv.reader( open('/home/pi/Desktop/Rally-Project/userdata/settings.csv', "rb"), delimiter=' ')
for row in settingsReader:
    Sbase = float(row[0])
    drive_s = float(row[1])/2
    simple_drive_mode = bool(row[2])


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
    return interrupted

def stopVeichle():
    print("alt")
    stop()

def left(i):
    print('left'+str(i))
    leftFor( angles[i-1]*drive_s )

def right(i):
    print('right'+str(i))
    rightFor( angles[i-1]*drive_s )

stop()

if not simple_drive_mode :
    models = [
              #'models/start.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/right1.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/right2.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/right3.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/left1.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/left2.pmdl',
              '/home/pi/Desktop/Rally-Project/userdata/left3.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/stop.pmdl'
              ]
    callbacks = [
                #start,
                lambda: right(1),
                lambda: right(2),
                lambda: right(3),
                lambda: left(1),
                lambda: left(2), 
                lambda: left(3), 
                stopVeichle]
else:
    models = [
              #'models/start.pmdl', 
              '/home/pi/Desktop/Rally-Project/userdata/right-simple.pmdl',
              '/home/pi/Desktop/Rally-Project/userdata/left-simple.pmdl',
              '/home/pi/Desktop/Rally-Project/userdata/stop.pmdl'
              ]
    callbacks = [
                #start,
                lambda: right(2),
                lambda: left(2),
                stopVeichle]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
