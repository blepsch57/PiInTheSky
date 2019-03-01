import RPi.GPIO as gpio
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_LSM303, math

from operator import truediv


led1Pin = 19
buttonPin = 18
led2Pin = 5
buzzerPin = 17 

shriekStarted = False

stage = 0
lastLoopTime = 0.0

blinkTimer = 0.0
shriekTimer = 0.0


def opAdd(*x):
    #print("opadd: args are {}".format(x))
    total = 0
    for i in x:
        #print("opadd: i is {}".format(i))
        total += i
    return total



delayConst = 0.01
delayTime = delayConst
totalAccel = [0.0, 0.0, 0.0]
count = 0
lsm303 = Adafruit_LSM303.LSM303()
while True:
    accel = [n/100 for n in lsm303.read()[0]]
    totalAccel = list(map(opAdd, totalAccel, accel))
    count += 1
    print(((totalAccel[0]**2+totalAccel[1]**2+totalAccel[2]**2)**0.5)/count)

