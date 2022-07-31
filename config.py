from distutils.command.config import config
from digitalio import DigitalInOut
import board
from enum import Enum

class SensorPosition(Enum):
    Side = 0
    Upward = 1
    Downward = 2

class SensorConfig:
    def __init__(self, pin, enabled, position = SensorPosition.Side, angle = -1):
        self.pin = pin
        self.digitalPin = DigitalInOut(pin)
        self.enabled = enabled
        self.position = position
        self.angle = angle

    def __str__(self):
        return "SensorConfig: pin=" + str(self.pin) + ", enabled=" + str(self.enabled) + ", position=" + str(self.position) + ", angle=" + str(self.angle)





class Config:
    BATERY_MIN = 3.3

    sensors = [
        SensorConfig(board.D4,  True, angle = 0),   # 0
        SensorConfig(board.D16, False, angle = 30),  # 1
        SensorConfig(board.D25, False, angle = 60),  # 2
        SensorConfig(board.D24, False, angle = 90),  # 3
        SensorConfig(board.D14, False, angle = 120), # 4
        SensorConfig(board.D15, False, angle = 150), # 5
        SensorConfig(board.D7, False, angle = 180), # 6
        SensorConfig(board.D18, False, angle = 210), # 7 
        SensorConfig(board.D8, True, angle = 240), # 8
        SensorConfig(board.D21, False, angle = 270), # 9
        SensorConfig(board.D12, False, angle = 300), # 10
        SensorConfig(board.D20, True, position=SensorPosition.Downward)
    ]


if __name__ == "__main__":
    print("Current configuration:")
    config = Config()
    print("Minimial batery voltage:", config.BATERY_MIN)
    for sensor in config.sensors:
        print(sensor)