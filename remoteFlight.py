#!/usr/bin/env python

from cmath import inf
from os import times
import time


from core.dronelib import DroneLib
from core.regulator import *



import socket            



     


finalAxis = [1000, 1500, 1500, 1500, 1000, 1000, 1000, 1000]

if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")
    


    print("Arming")
    drone.arm()
    
    
    
    s = socket.socket()        
    
    port = 12345               
    s.connect(('192.168.137.1', port))
    

    for x in range(100000000):
      

        message = s.recv(1024).decode()

        if message == "":
            break

        message = message.split("|")[0]
        message = message.split(",")

        try:
            for i in range(8):
                finalAxis[i] = int(message[i])

            print(finalAxis, end="\r")
            drone.update(finalAxis)
        except:
            pass

        time.sleep(0.01)
        
