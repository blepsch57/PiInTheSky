import RPi.GPIO as gpio
from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_LSM303, math

from operator import truediv
import time

led1Pin = 19
buttonPin = 18
led2Pin = 5
buzzerPin = 4

stage = 0
lastLoopTime = 0.0

blinkTimer = 0.0

delayConst = 0.01
delayTime = delayConst

lsm303 = Adafruit_LSM303.LSM303()
#lsm303.mag_rate = Adafruit_LSM303.MAGRATE_220
#lsm303.accel_rate = Adafruit_LSM303.ACCELRATE_220

arbitraryConstant = 1 #9.79937/10.422706978 #hopefully the ratio between the magnitude of measured and real acceleration

sample = 0
accelCalibrateSum = [0.0,0.0,0.0]
downVec = [0.0,0.0,0.0]
activationTimer = 0
timer = 0

deltaV = [0.0,0.0,0.0]

# gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(led1Pin, gpio.OUT)
gpio.setup(led2Pin, gpio.OUT)
gpio.setup(buttonPin, gpio.IN)
gpio.setup(buzzerPin, gpio.OUT)
stageDelayTimer = 0

gpio.output(buzzerPin, 1)
