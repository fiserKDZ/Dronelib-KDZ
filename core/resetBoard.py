#!/usr/bin/env python

from dronelib import DroneLib
import time



if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")
    print("First update sending")
    drone.update([0,1500,1500,1500,1000,1500,1000,2000])
    print("First update sent")
    drone.arm()
    message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))
    
    print(message)
    
    for x in range(100000000):
      message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))  
      print(message)
    