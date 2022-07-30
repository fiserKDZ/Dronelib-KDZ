#!/usr/bin/env python

from cmath import inf
from os import times
import time
import random


from core.dronelib import DroneLib
from core.regulator import *






if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")

    drone.arm()

    throttle = 1000

    for x in range(100000000):
        throttle += 0.01
        print(int(throttle))
        drone.update([int(throttle), 1500, 1500, 1500, 1000, 1500, 1000, 2000])
        message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))  
      
