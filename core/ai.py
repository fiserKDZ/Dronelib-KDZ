from algebra import *
from sensorArray import SensorArray

def calculateAvoidanceVector(self, sensorArray):
    result = Vector2D(0, 0)

    for sensor in sensorArray.sensors:
        if sensor.online:
            sensorAngle = sensor.config.angle
            #TODO calculate the sensorAngle in the correct direction