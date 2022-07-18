import os
from datetime import datetime
import time
import json

class Logger:
    defaultFolderPath = os.path.dirname(os.path.abspath(__file__)) + "/logs/"
    position = 0

    def fileLogName(self):
        dt = datetime.now()
        self.log_file = self.defaultFolderPath + "log_" + "{:%B-%d-%Y_%H-%M-%S}".format(dt) + ".txt"
        return self.log_file

    def open(self):
        #Open log file and parse it form json
        with open(self.log_file, "r") as f:
            self.data = json.load(f)
        self.position = 0
        print("Log opened from " + self.log_file)

    # To read the log file, add parameter log_file to the constructor
    # To write to the log file, use the log method without parameters
    def __init__(self, log_file=None):
        if log_file is None:
            self.fileLogName()
        else:
            self.log_file = log_file
            self.open()
        self.data = []
    
    def log(self, data):
        now = time.time()
        toAdd = {"time": now, "data": data}
        self.data.append(toAdd)

    def save(self):
        if len(self.data) > 0:
            if not os.path.exists(self.defaultFolderPath):
                os.makedirs(self.defaultFolderPath)
            with open(self.log_file, "a") as f:
                json.dump(self.data, f)
            self.data = []
        else:
            print("No data to save, skipping!")
            return
    
    def __del__(self):
        self.save()
        print("Log saved to " + self.log_file)
        print("Logger closed")
        return
    
    def __str__(self):
        res = "Logger_" + self.log_file + ", Data logged: " + str(len(self.data)) + "\nLast 10 lines:\n"
        for line in self.data[-10:]:
            res += line + "\n"
        return res
    
    def read(self):
        return self.data[self.position]

    def print(self):
        for line in self.data:
            print(line)

    def replayInit(self):
        self.position = 0
        self.startTime = time.time()
    
    def end(self):
        return self.position >= len(self.data)

    #Replay needs to be called faster than thsn its realtime speed
    def replay(self):
        if not self.end():
            if self.read()["time"] - self.data[0]["time"] < time.time() - self.startTime:
                ret = self.read()
                self.position += 1
                return ret
        else:
            print("Replay finished")
            return None
        return None
    

if __name__ == "__main__":
    # This is an example for calling Logger:
    logger = Logger()
    logger.log([0, 1, 2])
    time.sleep(0.1)
    logger.log([3, 4, 5])
    time.sleep(0.2)
    logger.log([6, 7, 8])
    logger.save()
    logger.open()
    logger.print()
    print("Running replay:")
    logger.replayInit()
    while not logger.end():
        data = logger.replay()
        if data is not None:
            print("Replay:", data)