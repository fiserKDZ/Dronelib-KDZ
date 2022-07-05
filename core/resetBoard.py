#!/usr/bin/env python

from dronelib import DroneLib
import time


from sensorArray import SensorArray

sa = SensorArray()


if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")

    message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))
    print("Recieved telemetry: ", message)

    drone.getData(drone.ANALOG)

    print("Battery: ", drone.analog['vbat'])


    print("Arming")
    drone.arm()
    
    now = time.time()
    for x in range(100000000):
      sa.read()
      #drone.sendCMD(16,DroneLib.SET_RAW_RC,[1000,1500,1500,1500,1000,1500,1000,2000],'HHHHHHHH')

      toAdd = time.time() - now

      throttle = int(1000 + (1000 * toAdd))
      if throttle > 1950:
        throttle = 1950
      
      if sa.sensors[0].value == -1:
        pval = 1500
      else:
        pval = 0.5 * (sa.sensors[0].value - 420) #Záporná pozor!!!
      rightleft = int(1500 - pval)

      if rightleft > 1550: rightleft = int(1550)
      if rightleft < 1450: rightleft = int(1450)

      print("Throttle", throttle, "   rightleft", rightleft, "   SensorVal =", sa.sensors[0].value)
      drone.update([1000, 1500, 1500,1500,1000,1500,1000,2000])
      message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))  
      print(message)
    