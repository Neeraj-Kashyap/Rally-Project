import RPi.GPIO as GPIO
import time

leftWheels = 15
rightWheels = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup( (leftWheels, rightWheels), GPIO.OUT)
#Our relays-board use an inverted logic: low signal trigger the relay.
#This explains why at first look the code can look "weird"

def straightFor( timeInSeconds ):
	GPIO.output( (leftWheels, rightWheels), False )
	time.sleep( timeInSeconds )
	GPIO.output( (leftWheels, rightWheels), True )

#To TURN LEFT use right wheels to gain the boost needed
def leftFor( timeInSeconds ):
	GPIO.output( rightWheels, False )
	time.sleep( timeInSeconds )
	GPIO.output( (leftWheels, rightWheels), True )
#To TURN RIGHT use right wheels to gain the boost needed
def rightFor( timeInSeconds ):
	GPIO.output( leftWheels, False )
	time.sleep( timeInSeconds )
	GPIO.output( (leftWheels, rightWheels), True )

straightFor( 0 )
leftFor( 2 )
straightFor(1)
#rightFor( 5 )
