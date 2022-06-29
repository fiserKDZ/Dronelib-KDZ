import board
import busio
import adafruit_vl53l0x
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

sensor.measurement_timing_budget = 20000

for x in range(1000):
    print('Range: {}mm'.format(sensor.range))