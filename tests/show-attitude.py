#!/usr/bin/env python


from dronelib import DroneLib
from sys import stdout

if __name__ == "__main__":

    drone = DroneLib("/dev/ttyACM0")
    try:
        while True:
            drone.getData(DroneLib.ATTITUDE)
            #print (drone.attitude) #uncomment for regular printing

            # Fancy printing (might not work on windows...)
            message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))
            stdout.write("\r%s" % message )
            stdout.flush()
            # End of fancy printing
    except Exception as error:
        print ("Error on Main: "+str(error))
