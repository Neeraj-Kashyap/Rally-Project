<<<<<<< HEAD
=======
from rpi import snowboydecoder
import sys
import signal
import RPi.GPIO as GPIO
import time
import random
import pyaudio
import wave

<<<<<<< HEAD:rpi-arm-raspbian-8.0-1.1.1/demo2.py

=======
>>>>>>> 0416192c13468ec2eb022d4d98b548a950c01276:rpi/__init__.py
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

def playSound():
    chunk = 1024
    # open the file for reading.
    wf = wave.open('../sounds/training.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream_ = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != '':
        stream_.write(data)
        data = wf.readframes(chunk)
    
    # cleanup stuff.
    stream_.close()    
    p.terminate()


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
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('alt')
    stop()

def ff():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('ff')
    leftFor(pi/2)
    rightFor(pi/4)
    leftFor(pi/5)
    rightFor(pi*2)
    stop()

# var pi is a global variable set to 180 deg
def left1():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    #playSound()
    print('Left1')
    leftFor(pi/12)
    

def left2():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('left2')
    leftFor(pi/4)

def left3():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('left3')
    leftFor(pi/3)

def left4():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('left4')
    leftFor(pi/2)

def right1():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('right1')
    rightFor(pi/12)

def right2():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('right2')
    rightFor(pi/4)

def right3():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('right3')
    rightFor(pi/3)

def right4():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('right4')
    rightFor(pi/2)

def duplex():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print('inversione')
    if random.randrange(0,1) < 0.5: # inversione a sinistra
        leftFor(pi)
    else:
        rightFor(pi) # inversione a destra


stop()
models = [
          #'models/start.pmdl', 
          'GoldModels/right1.pmdl', 
          'GoldModels/right2.pmdl', 
          'GoldModels/right3.pmdl', 
          'GoldModels/left1.pmdl', 
          'GoldModels/left2.pmdl',
<<<<<<< HEAD:rpi-arm-raspbian-8.0-1.1.1/demo2.py
          'GoldModels/left3.pmdl', 
=======
          'models/left3.pmdl', 
>>>>>>> 0416192c13468ec2eb022d4d98b548a950c01276:rpi/__init__.py
          'models/alt.pmdl'
          ]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [
            #start,
            right1,
            right2,
            right3,
            left1,
            left2, 
            left3, 
            alt
            ]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminam
>>>>>>> 3b31edc41ef3937797e5a58a332f2b339ce40feb
