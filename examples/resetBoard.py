#!/usr/bin/env python

from core.dronelib import DroneLib
from core.sensorArray import SensorArray

#sa = SensorArray()



if __name__ == "__main__":    
    #This automatically resets the drone
    drone = DroneLib("/dev/ttyACM0")
