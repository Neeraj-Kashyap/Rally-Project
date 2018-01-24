import snowboydecoder
import sys
import signal
import time
import random

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
    


def start():
    print('start')
    

def stop():
    print('stop')

# var pi is a global variable set to 180 deg
def left1():
    print('Left1')
    

def left2():
    print('left2')
    

def left3():
    print('left3')
    

def left4():
    print('left4')
    

def right1():
    print('right1')
    

def right2():
    print('right2')
    

def right3():
    print('right3')
    

def right4():
    print('right4')
    

def duplex():
    if random.randrange(0,1) < 0.5: # inversione a sinistra
        leftFor(pi)
    else:
        rightFor(pi) # inversione a destra



<<<<<<< HEAD
models = ['models/left1.pmdl','models/start.pmdl', 'models/stop.pmdl']
=======
models = ['../rpi-arm-raspbian-8.0-1.1.1/models/uno.pmdl','../rpi-arm-raspbian-8.0-1.1.1/models/due.pmdl', '../rpi-arm-raspbian-8.0-1.1.1/models/tre.pmdl']
>>>>>>> 3a5b1eb1857176e2dbdd52b0ca118cfe6f4a5be9

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [left1,
<<<<<<< HEAD
            start,
            stop]
=======
            left2,
            left3]
>>>>>>> 3a5b1eb1857176e2dbdd52b0ca118cfe6f4a5be9
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
