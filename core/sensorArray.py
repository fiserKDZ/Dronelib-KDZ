from digitalio import DigitalInOut
import board
import time
from adafruit_vl53l0x import VL53L0X

class vl53l0x:
    online = False
    powerPin = -1
    sensor = None
    id = -1
    value = -1

    def __init__(self, powerPin, address, id, i2c):
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
        except OSError as e:
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

    def __init__(self) -> None:

        
        xshut = [
            DigitalInOut(board.D4),
            DigitalInOut(board.D14),
            DigitalInOut(board.D15),
            DigitalInOut(board.D20),
            DigitalInOut(board.D17),
            DigitalInOut(board.D21),#5
            DigitalInOut(board.D26),
            DigitalInOut(board.D16),
            DigitalInOut(board.D19),
            DigitalInOut(board.D13),
            DigitalInOut(board.D12),#10
            DigitalInOut(board.D6),
            DigitalInOut(board.D27),#Down

        ]

        i2c = board.I2C()

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



class PIDController:
    def __init__(self, kp, ki, kd, min, max):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min = min
        self.max = max
        self.lastError = 0
        self.integral = 0
        self.lastTime = time.time()

    def update(self, error):
        now = time.time()
        dt = now - self.lastTime
        self.lastTime = now
        self.integral += error * dt
        derivative = (error - self.lastError) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.lastError = error
        if output > self.max:
            output = self.max
        elif output < self.min:
            output = self.min
        return output