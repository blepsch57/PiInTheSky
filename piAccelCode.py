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

logfile = open("logfile.txt", "w")
accelfile = open("accelfile.txt", "w")


def dot(vec1, vec2):
    assert (len(vec1)==len(vec2)), "You can't dot vectors of two different dimensions"
    total = 0
    for i in range(0, len(vec1)):
        total += vec1[i]*vec2[i]
    return total

def delayCalculate():
    global delayTime, lastLoopTime
    currentTime = time.time()
    delayTime = currentTime - lastLoopTime
    lastLoopTime = currentTime


def blink(stage):
    global blinkTimer
    if stage == 0:
        blinkTimer -= (blinkTimer if blinkTimer > 1.0 else 0.0)
        if blinkTimer > 0.5:
            gpio.output(led2Pin, False)
            gpio.output(led1Pin, True)
        else:
            gpio.output(led2Pin, False)
            gpio.output(led1Pin, False)
    elif stage == 1: 
        blinkTimer -= (blinkTimer if blinkTimer > 1.0 else 0.0)
        if blinkTimer > 0.5:
            gpio.output(led2Pin, True)
            gpio.output(led1Pin, False)
        else:
            gpio.output(led1Pin, False)
            gpio.output(led2Pin, False)
    elif stage == 2:
        blinkTimer -= (blinkTimer if blinkTimer > 2.0 else 0.0)
        #print("BlinkTimer: {}".format(blinkTimer))
        if blinkTimer > 0.5 and blinkTimer < 1.0:
            gpio.output(led1Pin, True)
            gpio.output(led2Pin, False)
            #print('1ed')
        elif blinkTimer > 1.5: 
            gpio.output(led2Pin, True)
            gpio.output(led1Pin, False)
            #print('l3d')
        else:
            gpio.output(led1Pin, False)
            gpio.output(led2Pin, False)
    blinkTimer += delayTime
            


def magnitude(vec):
    return (sum([n**2 for n in vec]))**0.5

def shriek():
    gpio.output(led1Pin, True)
    gpio.output(led2Pin, True)
    gpio.output(buzzerPin, True)
    print("shrieking -__--_--_-__-_-_---_---_-_-----_-_-----_-_-_-_-----_--__-_")
    logfile.write("start shriek at time {}\n".format(time.time()))

def unshriek():
    gpio.output(led1Pin, False)
    gpio.output(led2Pin, False)
    gpio.output(buzzerPin, False)
    logfile.write("end shriek at time {}\n".format(time.time()))

def opAdd(*x):
    #print("opadd: args are {}".format(x))
    total = 0
    for i in x:
        #print("opadd: i is {}".format(i))
        total += i
    return total

while True:
    
    stage = 0
    lastLoopTime = 0.0

    blinkTimer = 0.0
    shriekTimer = 0.0

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

    stageDelayTimer = 0

    lastLoopTime = time.time()
    gpio.output(buzzerPin, False)

    logfile.write("stage 0 initialized at time {}\n".format(time.time()))
    lastLoopTime = time.time()
    while stage == 0:
        delayCalculate()
        stage += not gpio.input(buttonPin)
        blink(stage)
        print("stage 0")
        time.sleep(delayConst)

    logfile.write("stage 1 initialized at time {}\n".format(time.time()))
    while stage == 1:
        delayCalculate()
        if not gpio.input(buttonPin) and stageDelayTimer > 3.0:
            stage += 1
        blink(stage)
        accel = [n*arbitraryConstant/100.0 for n in lsm303.read()[0]]
        accelCalibrateSum = list( map(opAdd, accelCalibrateSum, [n/100.0 for n in accel]) )
        sample += 1
        print("stage 1, accel = {}".format(accel))
        stageDelayTimer += delayTime
        time.sleep(delayConst)

    blinkTimer = 0.0
    stageDelayTimer = 0.0
    magnitudeFactor = magnitude(accelCalibrateSum)
    downVec = [-n/magnitudeFactor for n in accelCalibrateSum]
    accelfile.write("downVec = {}\n".format(downVec))

    
    deltaV = [0.0,0.0,0.0]

    logfile.write("stage 2 initialized at time {}. downvec = {}\n".format(time.time(), downVec))
    while stage == 2:
        delayCalculate()
        accel = [n*arbitraryConstant/100.0 for n in lsm303.read()[0]]
        blink(stage)
        if math.acos(dot(accel, [-n for n in downVec])/(magnitude(downVec)*magnitude(accel))) > 3.141592653589793238462643383/4.0 or (not gpio.input(buttonPin) and stageDelayTimer >0.5):
            stage += 1
            deltaV = list(map(opAdd, deltaV, [n*delayTime for n in accel], [n*9.8*delayTime for n in downVec]))
        print("stage 2, accel = {}".format(accel))
        stageDelayTimer += delayTime
        time.sleep(delayConst)
    
    stageDelayTimer = 0.0
    blinkTimer = 0.0
    activationTimer = 0.0

    shriekStarted = False
    shriekTimer = 0.0

    logfile.write("stage 3 initialized at time {}\n".format(time.time()))
    while stage == 3:
        if not gpio.input(buttonPin) and stageDelayTimer > 3.0:
            stage += 1
        delayCalculate()
        accel = [n*arbitraryConstant/100.0 for n in lsm303.read()[0]]
        deltaV = list(map(opAdd, deltaV, [n*delayTime for n in accel], [n*9.8*delayTime for n in downVec]))
        accelfile.write("time: {}, deltaV = {} ".format(time.time(), deltaV))
        accelfile.write("vertical component = {}\n".format(dot(deltaV, downVec)))
        if shriekTimer < 1.0 and activationTimer>0.25 and abs(dot(deltaV, downVec)) < 10:
            if shriekStarted == False:
                logfile.write("shrieking at time {}, deltaV {} m/s\n".format(time.time(), deltaV))
            shriekStarted = True
            shriek()
        elif shriekTimer > 1.0:
            unshriek()
        activationTimer += delayTime 
        stageDelayTimer += delayTime
        shriekTimer += shriekStarted*delayTime
        print("stage 3, accel = {}, deltaV = {}, activated = {}\n".format(accel, deltaV, activationTimer>0.5/delayTime))
        time.sleep(delayConst)
