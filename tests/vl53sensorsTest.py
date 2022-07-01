import time
import VL53L0X
import RPi.GPIO as GPIO





sensors = [23, 24] #SEM STAČÍ NASTAVIT XSHUT PINY





#Reffering to this page: https://github.com/johnbryanmoore/VL53L0X_rasp_python/blob/master/python/VL53L0X_multi_example.py

addresses = [0x2B, 0x2D, 0x2F, 0x31, 0x33, 0x35, 0x37, 0x39, 0x3B, 0x3D, 0x3F, 0x41, 0x43, 0x45, 0x47, 0x49, 0x4B, 0x4D, 0x4F, 0x51]

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
for sensor in sensors:
    GPIO.setup(sensor, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
for sensor in sensors:
    GPIO.setup(sensor, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.5)

# Create one object per VL53L0X passing the address to give to
tofs = [VL53L0X.VL53L0X(i2c_address=addresses[0])]



# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 


for i in range(len(sensors)):
    GPIO.output(sensors[i], GPIO.HIGH)
    time.sleep(0.50)
    tofs.append(VL53L0X.VL53L0X(i2c_address=addresses[i]))
    tofs[len(tofs)-1].start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tofs[0].get_timing()
if (timing < 20000):
    timing = 20000
print ("INIT FINISHED!\nTiming %d ms" % (timing/1000))

for count in range(100):
    for tof in tofs:
        distance = tof.get_distance()
        if (distance > 0):
            print ("sensor %d - %d mm, %d cm, iteration %d" % (tof.my_object_number, distance, (distance/10), count))
        else:
            print ("%d - Error" % tof.my_object_number)

    time.sleep(timing/1000000.00)


for sensor in sensors:
    GPIO.output(sensor, GPIO.LOW)
for tof in tofs:
    tof.stop_ranging()