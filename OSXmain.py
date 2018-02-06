from osx import snowboydecoder
import sys
import signal
import time
import random
import csv
#___________________________________________________________________________

#read settings file 
settingsReader = csv.reader( open('app/toRPI/settings.csv', "rb"), delimiter=' ')
for row in settingsReader:
    Sbase = row[0]
    drive_s = row[1]
    simple = row[2]


pi = 2*1.30

interrupted = False
angles = [pi/12, pi/6, pi/3]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def left(i):
    print('left'+str(i))
    

def right(i):
    print('right'+str(i))

def alt():
    print("alt" ) 

models = [
          #'models/start.pmdl', 
          'models/gold/right1.pmdl', 
          'models/gold/right2.pmdl', 
          'models/gold/right3.pmdl', 
          'models/gold/left1.pmdl', 
          'models/gold/left2.pmdl',
          'models/gold/left3.pmdl', 
          'models/alt.pmdl'
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
