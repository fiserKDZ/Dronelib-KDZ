from cmath import inf
from os import times
from dronelib import DroneLib
import time



if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")


    drone.getData(drone.ALTITUDE) #Proč nepříjmul data? wtf?
    message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))
    print("Recieved telemetry: ", message)

    drone.getData(drone.PID)

    print(drone.PIDcoef)