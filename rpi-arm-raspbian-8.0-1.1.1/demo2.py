import snowboydecoder
import sys
import signal
import RPi.GPIO as GPIO
import time
import random

pi = 3*1.30
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

def straightFor( timeInSeconds ):
    GPIO.output( (leftWheels, rightWheels), False )
    time.sleep( timeInSeconds )
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


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def getReady():
    print('Car worked')
    straightFor(0.3)

def start():
    print('start')
    straight()

def alt():
    print('alt')
    stop()

# var pi is a global variable set to 180 deg
def left1():
    print('Left1')
    leftFor(pi/12)

def left2():
    print('left2')
    leftFor(pi/5)

def left3():
    print('left3')
    leftFor(pi/3)

def left4():
    print('left4')
    leftFor(pi/2)

def right1():
    print('right1')
    rightFor(pi/12)

def right2():
    print('right2')
    rightFor(pi/5)

def right3():
    print('right3')
    rightFor(pi/3)

def right4():
    print('right4')
    rightFor(pi/2)

def duplex():
    print('inversione')
    if random.randrange(0,1) < 0.5: # inversione a sinistra
        leftFor(pi)
    else:
        rightFor(pi) # inversione a destra


stop()
models = ['models/start.pmdl', 
          'models/destra1.pmdl', 
          'models/destra2.pmdl', 
          'models/destra3.pmdl', 
          'models/sinistra1.pmdl', 
          'models/sinistra2.pmdl',
          'models/sinistra3.pmdl', 
          'models/alt.pmdl']

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [.55]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [start,
            right1,
            right2,
            right3,
            left1,
            left2, 
            left3, 
            alt]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
