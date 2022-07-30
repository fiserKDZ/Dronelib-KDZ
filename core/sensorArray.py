from digitalio import DigitalInOut
import board
import time
from adafruit_vl53l0x import VL53L0X
from config import *

config = Config()



class vl53l0x:
    online = False
    powerPin = -1
    sensor = None
    id = -1
    value = -1
    config = None

    def __init__(self, powerPin, address, id, i2c, config = None):
        self.config = config
        self.powerPin = powerPin
        self.powerPin.value = True
        self.id = id
        try:   
            self.sensor = VL53L0X(i2c)     
            self.online = True
            self.sensor.set_address(address)
            self.sensor.__enter__()
#            self.sensor.measurement_timing_budget = 33000
            self.sensor.measurement_timing_budget = 20000
            print("SUCCESS: Sensor id: " + str(id) + " is ONLINE!")
        except ValueError as e:
            print("ERROR: Sensor id: " + str(id) + " is OFFLINE:", e)
            powerPin.value = False
            self.online = False

    def read(self):
        if self.online:
            try:
                self.value = self.sensor.range
            except OSError as e:
                #self.online = False
                #TODO Reboot the sensor on new thread!
                print(time.time(), "Sensor disconnected :( ... TODO ... id=" + str(self.id))
                #self.powerPin.value = False
                self.value = -1
                return -1
            if self.value > 2000:
                self.value = -1
            if self.value < 1:
                self.value = -1
            return self.value
        else:
            return -1
    
    def pvalue(self):
        offset = 1000
        if self.online and self.value != -1:
            if self.value > offset:
                return 0
            return offset - self.value
        else:
            return 0


class SensorArray:
    sensors = []

    def __init__(self):
        
        offline = [
            DigitalInOut(board.D7),
            DigitalInOut(board.D21),
            DigitalInOut(board.D8),
            DigitalInOut(board.D12),
            DigitalInOut(board.D4),
            DigitalInOut(board.D16),
            DigitalInOut(board.D25),#5
            DigitalInOut(board.D24),
            DigitalInOut(board.D14),
            DigitalInOut(board.D15),
            DigitalInOut(board.D18),#10
        ]

        xshut = [DigitalInOut(board.D20),#DOWN

        ]

        i2c = board.I2C()

        for power_pin in offline:
            power_pin.switch_to_output(value=False)
        for power_pin in xshut:
            # make sure these pins are a digital output, not a digital input
            power_pin.switch_to_output(value=False)
            # These pins are active when Low, meaning:
            #   if the output signal is LOW, then the VL53L0X sensor is off.
            #   if the output signal is HIGH, then the VL53L0X sensor is on.
        # all VL53L0X sensors are now off

        # initialize a list to be used for the array of VL53L0X sensors
        self.sensors = []

        # now change the addresses of the VL53L0X sensors
        for i, powerPin in enumerate(xshut):
            self.sensors.append(vl53l0x(powerPin, i + 0x30, i, i2c))

    def read(self):
        for sensor in self.sensors:
            sensor.read()

    def printHead(self):
        for sensor in range(len(self.sensors)):
            print("{0: >8} ".format(str(sensor) + ". TOF"), end="")
        print(" ")
    def print(self):
        for sensor in self.sensors:
            print("{0: >8} ".format(round(sensor.value)), end="")
        
        print ("", end="\r")

    def bottomSensor(self):
        return self.sensors[-1]

        
# there is a helpful list of pre-designated I2C addresses for various I2C devices at
# https://learn.adafruit.com/i2c-addresses/the-list
# According to this list 0x30-0x34 are available, although the list may be incomplete.
# In the python REPR, you can scan for all I2C devices that are attached and detirmine
# their addresses using:
#   >>> import board
#   >>> i2c = board.I2C()
#   >>> if i2c.try_lock():
#   >>>     [hex(x) for x in i2c.scan()]
#   >>>     i2c.unlock()



# DEMO - run this code to see the output of the sensor array
if __name__ == "__main__":
    sa = SensorArray()
    sa.printHead()
    while True:
        sa.read()
        sa.print()
        #time.sleep(0.05)