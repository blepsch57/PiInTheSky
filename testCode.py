delayTime = 0.0
lastLoopTime = 0.0

import time


def delayCalculate():
    global delayTime, lastLoopTime #yeet
    currentTime = time.time()
    delayTime = currentTime - lastLoopTime
    lastLoopTime = currentTime


lastLoopTime = time.time()
while True:
    delayCalculate()
    print(delayTime)
    time.sleep(1.0)


