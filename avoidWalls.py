#!/usr/bin/env python

from cmath import inf
from os import times
import time


from core.dronelib import DroneLib
from core.sensorArray import SensorArray
from core.regulator import *

sa = SensorArray()





if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")
    


    print("Arming")
    drone.arm()
    
    
    lasterror = 0
    lastThrottle = []

    now = time.time()
    timestamp = time.time()
    def printDiff(timestamp, timenow, message):
        print(message, "--- NOW:", timenow, "Diff: ", round(timenow - timestamp, 6))
        timestamp = timenow
        return timestamp

    for x in range(100000000):
      timestamp = printDiff(timestamp, time.time(), "1")

      sa.read()
      #drone.sendCMD(16,DroneLib.SET_RAW_RC,[1000,1500,1500,1500,1000,1500,1000,2000],'HHHHHHHH')

      timestamp = printDiff(timestamp, time.time(), "2")

      if sa.sensors[12].value == -1:
        throttle = 1400

      else:
        error = (2000 - sa.sensors[12].value)
        throttle = 1500 + 0.04 * error + 0.5 * (error - lasterror)
        lasterror = error
        if throttle < 1400:
          throttle = 1400


      toAdd = time.time() - now
      throttleLimit = int(1000 + (1000 * toAdd))
      if throttleLimit > 1800:
        throttleLimit = 1800
      if throttle > throttleLimit:
        throttle = throttleLimit
      


      penale1 = 1.1
      penale2 = 1.05

      minRight = inf
      if sa.sensors[4].value != -1 and penale1 * sa.sensors[4].value < minRight:
        minRight = penale1 * sa.sensors[4].value
      if sa.sensors[5].value != -1 and penale2 * sa.sensors[5].value < minRight:
        minRight = penale2 * sa.sensors[5].value
      if sa.sensors[6].value != -1 and sa.sensors[6].value < minRight:
        minRight = sa.sensors[6].value
      if sa.sensors[7].value != -1 and penale2 * sa.sensors[7].value < minRight:
        minRight = penale2 * sa.sensors[7].value
      if sa.sensors[8].value != -1 and penale1 * sa.sensors[8].value < minRight:
        minRight = penale1 * sa.sensors[8].value

      minLeft = inf
      if sa.sensors[10].value != -1 and penale1 * sa.sensors[10].value < minLeft:
        minLeft = penale1 * sa.sensors[10].value
      if sa.sensors[11].value != -1 and penale2 * sa.sensors[11].value < minLeft:
        minLeft = penale2 * sa.sensors[11].value
      if sa.sensors[0].value != -1 and sa.sensors[0].value > minLeft:
        minLeft = sa.sensors[0].value
      if sa.sensors[1].value != -1 and penale2 * sa.sensors[1].value < minLeft:
        minLeft = penale2 * sa.sensors[1].value
      if sa.sensors[2].value != -1 and penale1 * sa.sensors[2].value < minLeft:
        minLeft = penale1 * sa.sensors[2].value

      if minLeft > 500:
        minLeft = 500
      if minRight > 500:
        minRight = 500

      rightleft = 0.5 * (minRight - minLeft)



      if rightleft > 75:
        rightleft = 75
      if rightleft < -75:
        rightleft = -75
      if sa.sensors[12].value < 300 and sa.sensors[12].value > 0:
        rightleft = 0

      minFront = inf
      if sa.sensors[7].value != -1 and penale1 * sa.sensors[7].value < minFront:
        minFront = penale1 * sa.sensors[7].value
      if sa.sensors[8].value != -1 and penale2 * sa.sensors[8].value < minFront:
        minFront = penale2 * sa.sensors[8].value
      if sa.sensors[9].value != -1 and sa.sensors[9].value < minFront:
        minFront = sa.sensors[9].value
      if sa.sensors[10].value != -1 and penale2 * sa.sensors[10].value < minFront:
        minFront = penale2 * sa.sensors[10].value
      if sa.sensors[11].value != -1 and penale1 * sa.sensors[11].value < minFront:
        minFront = penale1 * sa.sensors[11].value

      minBack = inf
      if sa.sensors[1].value != -1 and penale1 * sa.sensors[1].value < minBack:
        minBack = penale1 * sa.sensors[1].value
      if sa.sensors[2].value != -1 and penale2 * sa.sensors[2].value < minBack:
        minBack = penale2 * sa.sensors[2].value
      if sa.sensors[3].value != -1 and sa.sensors[3].value < minBack:
        minBack = sa.sensors[3].value
      if sa.sensors[4].value != -1 and penale2 * sa.sensors[4].value < minBack:
        minBack = penale2 * sa.sensors[4].value
      if sa.sensors[5].value != -1 and penale1 * sa.sensors[5].value < minBack:
        minBack = penale1 * sa.sensors[5].value

      if minFront > 500:
        minFront = 500
      if minBack > 500:
        minBack = 500

      frontback = 0.5 * (minFront - minBack)


      if frontback > 75:
        frontback = 75
      if frontback < -75:
        frontback = -75
      if sa.sensors[12].value < 300 and sa.sensors[12].value > 0:
        frontback = 0




      
      timestamp = printDiff(timestamp, time.time(), "3")

      throttle = int(throttle)
      lastThrottle.append(throttle)
      if len(lastThrottle) > 5:
        lastThrottle.pop(0)
      avgThrottle = int(sum(lastThrottle) / len(lastThrottle))
      print("Throttle", avgThrottle, "   SensorVal =", sa.sensors[12].value, "   RightLeft =", rightleft, minRight, minLeft, "  Forntback", frontback, minFront, minBack)
      drone.update([throttle, int(1508 + rightleft), int(1515 + frontback),1500,1000,1500,1000,2000])
      timestamp = printDiff(timestamp, time.time(), "4")
      #message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))  
      #print(message)
    