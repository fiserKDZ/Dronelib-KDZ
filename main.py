from core.dronelib import DroneLib
from core.sensorArray import SensorArray


sa = SensorArray()



class Vector:
    x = 0
    y = 0
    z = 0

    def limit(self, val):
        if self.x > val: self.x = val
        if self.x < -1 * val: self.x = -1 * val
        if self.y > val: self.y = val
        if self.y < -1 * val: self.y = -1 * val
        if self.z > val: self.z = val
        if self.z < -1 * val: self.z = -1 * val

while True:
    sa.read()
    pval = Vector()

    for sensor in sa.sensors:
        if sensor.id == 0:
            pval.y -= sensor.pvalue()
        elif sensor.id == 1:
            pval.x -= 0.7 * sensor.pvalue()
            pval.y -= 0.7 * sensor.pvalue()
        elif sensor.id == 2:
            pval.x -= sensor.pvalue()
        elif sensor.id == 3:
            pval.x -= 0.7 * sensor.pvalue()
            pval.y += 0.7 * sensor.pvalue()
        elif sensor.id == 4:
            pval.y += sensor.pvalue()
        elif sensor.id == 5:
            pval.x += 0.7 * sensor.pvalue()
            pval.y += 0.7 * sensor.pvalue()
        elif sensor.id == 6:
            pval.x += sensor.pvalue()
        elif sensor.id == 7:
            pval.x += 0.7 * sensor.pvalue()
            pval.y -= 0.7 * sensor.pvalue()
        elif sensor.id == 8:
            height = 500
            pval.z = height - sensor.value
            if pval.z > height:
                pval.z = height
            if pval.z < -height:
                pval.z = -height
    
    #pval.limit(400)
    
    print("Values: {0: >5} {1: >5} {2: >5}".format(round(pval.x), round(pval.y), round(pval.z)), end="\r")








if __name__ == "__main__":    
    drone = DroneLib("/dev/ttyACM0")
    print("First update sending")
    drone.update([1800,1500,1500,1500,1000,1500,1000,2000])
    print("First update sent")
    drone.arm()
    message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))
    
    print(message)
    
    for x in range(100000000):
      drone.sendCMD(16,DroneLib.SET_RAW_RC,[1800,1500,1500,1500,1000,1500,1000,2000],'HHHHHHHH')
      message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(drone.attitude['angx']),float(drone.attitude['angy']),float(drone.attitude['heading']),float(drone.attitude['elapsed']))  
      print(message)
    