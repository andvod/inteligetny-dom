
import RPi.GPIO as GPIO

##constants
PinActivity = 7   # default pin to output data is 7
LightCardOpen = 11
LightCardError = 36
ButtonClick = 38

VerificationInputPin = 12
VerificationOutputPin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PinActivity, GPIO.OUT)
GPIO.output(PinActivity, True)

TimeRuning = 100
