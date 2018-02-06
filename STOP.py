import RPi.GPIO as GPIO
# pin per rasby
leftWheels = 15
rightWheels = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup( (leftWheels, rightWheels), GPIO.OUT)

GPIO.output( (leftWheels, rightWheels), True )
