#!/usr/bin/env python

import serial, time, struct

class DroneLib:
    #Commands:
    ARMING_DISABLED = 99
    IDENT = 100
    STATUS = 101
    RAW_IMU = 102
    SERVO = 103
    MOTOR = 104
    RC = 105
    RAW_GPS = 106
    COMP_GPS = 107
    ATTITUDE = 108
    ALTITUDE = 109
    ANALOG = 110
    RC_TUNING = 111
    PID = 112
    BOX = 113
    MISC = 114
    MOTOR_PINS = 115
    BOXNAMES = 116
    PIDNAMES = 117
    WP = 118
    BOXIDS = 119
    RC_RAW_IMU = 121
    SET_RAW_RC = 200
    SET_RAW_GPS = 201
    SET_PID = 202
    SET_BOX = 203
    SET_RC_TUNING = 204
    ACC_CALIBRATION = 205
    MAG_CALIBRATION = 206
    SET_MISC = 207
    RESET_CONF = 208
    SET_WP = 209
    SWITCH_RC_SERIAL = 210
    IS_SERIAL = 211
    DEBUG = 254
    VTX_CONFIG = 88
    VTX_SET_CONFIG = 89
    EEPROM_WRITE = 250
    REBOOT = 68

    #CONFIGURATION

    BATERY_MIN = 6.5 #Minimal battery voltage

    DEFAULT_STICK_POSITION = [1000,1500,1500,1500,1000,1500,1000,2000]

    def __init__(self, serPort):
        print("Connecting the drone on port: " + serPort)
        self.PIDcoef = {'rp':0,'ri':0,'rd':0,'pp':0,'pi':0,'pd':0,'yp':0,'yi':0,'yd':0}
        self.rcChannels = {'roll':0,'pitch':0,'yaw':0,'throttle':0,'elapsed':0,'timestamp':0}
        self.rawIMU = {'ax':0,'ay':0,'az':0,'gx':0,'gy':0,'gz':0,'mx':0,'my':0,'mz':0,'elapsed':0,'timestamp':0}
        self.motor = {'m1':0,'m2':0,'m3':0,'m4':0,'elapsed':0,'timestamp':0}
        self.attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
        self.altitude = {'estalt':0,'vario':0,'elapsed':0,'timestamp':0}
        self.message = {'angx':0,'angy':0,'heading':0,'roll':0,'pitch':0,'yaw':0,'throttle':0,'elapsed':0,'timestamp':0}
        self.vtxConfig = {'device':0, 'band':0, 'channel':0, 'power':0, 'pit':0, 'unknown':0}
        self.analog = {'vbat':0, 'powerMeter':0, 'rssi':0, 'txPower':0, 'elapsed':0, 'timestamp':0}
        self.temp = ();
        self.temp2 = ();
        self.elapsed = 0
        self.PRINT = 1

        self.ser = serial.Serial()
        self.ser.port = serPort
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2
        """Time to wait until the board becomes operational"""
        wakeup = 2
        try:
            self.ser.open()
            if self.PRINT:
                print ("Waking up board on "+self.ser.port+"...")
            for i in range(1,wakeup):
                if self.PRINT:
                    print ("Wakeup:", wakeup-i)
                    time.sleep(1)
                else:
                    time.sleep(0.1)
        except Exception as error:
            print ("\n\nError opening "+self.ser.port+" port.\n"+str(error)+"\n\n")

        
    
        print("Rebooting the board ... eta 3s")
        self.reboot()
        self.update(self.DEFAULT_STICK_POSITION)
        print("Drone READY!")

    def sendCMD(self, data_length, code, data, data_format):
        checksum = 0
        total_data = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), data_length, code] + data
        #print("s - original", total_data)
        for i in struct.pack('<2B' + data_format, *total_data[3:len(total_data)]):
            checksum = checksum ^ i
        total_data.append(checksum)
        try:
            b = None
            #print("sending:", struct.pack('<3c2B'+ data_format + 'B', *total_data))
            b = self.ser.write(struct.pack('<3c2B'+ data_format + 'B', *total_data))
        except Exception as error:
            print ("\n\nError in sendCMD.")
            print ("("+str(error)+")\n\n")
            pass
            
    def sendCMD_u(self, hexa):
        tosend = bytes.fromhex(hexa)
        try:
            b = None
            b = self.ser.write(tosend)
            """
            while True:
                header = self.ser.read().decode('utf-8')
                if header == '$':
                    header = header+self.ser.read(2).decode('utf-8')
                    break"""
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            self.ser.flushInput()
            self.ser.flushOutput()
        except Exception as error:
            pass #This is not finished, clean it yourself if you can :)
    
    def arm(self):
        def parseCommandsFromFile(filename):
            commands = [] #Tuple:   timestamp, code, message
            with open(filename) as f:
                for line in f:
                    loc = line.find("++")
                    if loc != -1:
                        loc2 = line.find("//")
                        loc3 = line.find("**")
                        crop1 = line[loc+2:loc2]
                        crop2 = line[loc2+2:loc3]
                        crop3 = line[loc3+2:].replace("\n", "")
                        a =(crop1, crop2, crop3)
                        commands.append(a)
            return commands
            
        commands = parseCommandsFromFile("arm.seq")
        begining = int(commands[0][0]) - 5
        counter = 0
        
        now = time.time()
        while counter < len(commands)-1:
            try:
                if time.time() > now + (int(commands[counter][0]) - begining) / 1000:
                    #print("sent", commands[counter][0])
                    self.sendCMD_u(commands[counter][2])
                    counter += 1
                    i = (time.time()-now)/ 5.77 * 100
                    print('ARMING [%d%%]\r'%i, end="")

            except TypeError as error:
                print ("Error on Main: "+str(error))
        print("ARMED [100%]")
    
    def update(self, sticks):
        try:
            #Roll, Pitch, Yaw, Throttle, AUX1, AUX2, AUX3, AUX4
            self.sendCMD(16,DroneLib.SET_RAW_RC,sticks,'HHHHHHHH')
            
            #while True:
            #    header = self.ser.read().decode('utf-8')
            #    if header == '$':
            #        header = header+self.ser.read(2).decode('utf-8')
            #        break
            #datalength = struct.unpack('<b', self.ser.read())[0]
            #code = struct.unpack('<b', self.ser.read())
            #data = self.ser.read(datalength)
            self.ser.flushInput()
            self.ser.flushOutput()

            #self.getData(self.ATTITUDE)
        except Exception as e:
            print("Drone communication error :::", e)

    def disarm(self):
        timer = 0
        start = time.time()
        while timer < 6:
            try:
                data = [1500,1500,1500,1000,1000,1500,1000,1000]
                self.sendCMD(16,DroneLib.SET_RAW_RC,data,'HHHHHHHH')
                
                
                while True:
                    header = self.ser.read().decode('utf-8')
                    if header == '$':
                        header = header+self.ser.read(2).decode('utf-8')
                        break
                datalength = struct.unpack('<b', self.ser.read())[0]
                code = struct.unpack('<b', self.ser.read())
                data = self.ser.read(datalength)
                self.ser.flushInput()
                self.ser.flushOutput()
            
                #print("recieved", data)
                #print(data.decode(encoding='utf8'))
                
                time.sleep(0.01)
                timer = timer + (time.time() - start)
                start =  time.time()
            except Exception as e:
                print("disarming err", e)
    
    def setPID(self,pd):
        nd=[]
        for i in np.arange(1,len(pd),2):
            nd.append(pd[i]+pd[i+1]*256)
        data = pd
        print ("PID sending:", data)
        self.sendCMD(30,DroneLib.SET_PID,data)
        self.sendCMD(0,DroneLib.EEPROM_WRITE,[])

    def setVTX(self,band,channel,power):
        band_channel = ((band-1) << 3)|(channel-1)
        t = None
        while t == None :
            t = self.getData(DroneLib.VTX_CONFIG)
        different = (self.vtxConfig['band'] != band) | (self.vtxConfig['channel'] != channel) | (self.vtxConfig['power'] != power)
        data = [band_channel,power,self.vtxConfig['pit']]
        while different :
            self.sendCMD(4,DroneLib.VTX_SET_CONFIG,data, 'H2B')
            time.sleep(1)
            self.sendCMD(0,DroneLib.EEPROM_WRITE,[],'')
            self.ser.close()
            time.sleep(3)
            self.ser.open()
            time.sleep(3)
            t = None
            while t == None :
                t = self.getData(DroneLib.VTX_CONFIG)
            print(t)
            different = (self.vtxConfig['band'] != band) | (self.vtxConfig['channel'] != channel) | (self.vtxConfig['power'] != power)

    """Function to receive a data packet from the board"""
    def getData(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,cmd,[],'')
            while True:
                header = self.ser.read().decode('utf-8')
                if header == '$':
                    header = header+self.ser.read(2).decode('utf-8')
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            
            self.ser.flushInput()
            self.ser.flushOutput()
            elapsed = time.time() - start
            if cmd == DroneLib.ATTITUDE:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)                
                self.attitude['angx']=float(temp[0]/10.0)
                self.attitude['angy']=float(temp[1]/10.0)
                self.attitude['heading']=float(temp[2])
                self.attitude['elapsed']=round(elapsed,3)
                self.attitude['timestamp']="%0.2f" % (time.time(),) 
                return self.attitude
            elif cmd == DroneLib.ALTITUDE:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                self.altitude['estalt']=float(temp[0])
                self.altitude['vario']=float(temp[1])
                self.altitude['elapsed']=round(elapsed,3)
                self.altitude['timestamp']="%0.2f" % (time.time(),) 
                return self.altitude
            elif cmd == DroneLib.RC:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                self.rcChannels['roll']=temp[0]
                self.rcChannels['pitch']=temp[1]
                self.rcChannels['yaw']=temp[2]
                self.rcChannels['throttle']=temp[3]
                self.rcChannels['elapsed']=round(elapsed,3)
                self.rcChannels['timestamp']="%0.2f" % (time.time(),)
                return self.rcChannels
            elif cmd == DroneLib.RAW_IMU:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                self.rawIMU['ax']=float(temp[0])
                self.rawIMU['ay']=float(temp[1])
                self.rawIMU['az']=float(temp[2])
                self.rawIMU['gx']=float(temp[3])
                self.rawIMU['gy']=float(temp[4])
                self.rawIMU['gz']=float(temp[5])
                self.rawIMU['mx']=float(temp[6])
                self.rawIMU['my']=float(temp[7])
                self.rawIMU['mz']=float(temp[8])
                self.rawIMU['elapsed']=round(elapsed,3)
                self.rawIMU['timestamp']="%0.2f" % (time.time(),)
                return self.rawIMU
            elif cmd == DroneLib.MOTOR:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                self.motor['m1']=float(temp[0])
                self.motor['m2']=float(temp[1])
                self.motor['m3']=float(temp[2])
                self.motor['m4']=float(temp[3])
                self.motor['elapsed']="%0.3f" % (elapsed,)
                self.motor['timestamp']="%0.2f" % (time.time(),)
                return self.motor
            elif cmd == DroneLib.PID:
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                dataPID=[]
                if len(temp)>1:
                    d=0
                    for t in temp:
                        dataPID.append(t%256)
                        dataPID.append(t/256)
                    for p in [0,3,6,9]:
                        dataPID[p]=dataPID[p]/10.0
                        dataPID[p+1]=dataPID[p+1]/1000.0
                    self.PIDcoef['rp']= dataPID=[0]
                    self.PIDcoef['ri']= dataPID=[1]
                    self.PIDcoef['rd']= dataPID=[2]
                    self.PIDcoef['pp']= dataPID=[3]
                    self.PIDcoef['pi']= dataPID=[4]
                    self.PIDcoef['pd']= dataPID=[5]
                    self.PIDcoef['yp']= dataPID=[6]
                    self.PIDcoef['yi']= dataPID=[7]
                    self.PIDcoef['yd']= dataPID=[8]
                return self.PIDcoef
            elif cmd == DroneLib.VTX_CONFIG:
                if datalength > 1:
                    temp = struct.unpack('<bbbbb',data)
                    self.vtxConfig['device'] = temp[0]
                    self.vtxConfig['band'] = temp[1]
                    self.vtxConfig['channel'] = temp[2]
                    self.vtxConfig['power'] = temp[3]
                    self.vtxConfig['pit'] = temp[4]
                    self.vtxConfig['unknown'] = 0
                    return self.vtxConfig
                else:
                    temp = struct.unpack('<b',data)
                    self.vtxConfig['unknown'] = temp[0]
                    return self.vtxConfig
            
            elif cmd == DroneLib.ANALOG:
                print("!!! Recieved STATUS, data length:", datalength)
                temp = struct.unpack('<'+'h' + 'b' + 'h' + 'h' + 'h',data)
                self.analog['vbat']=temp[0]/10
                #self.analog['powerMeter']=temp[1] #Random byte appears here idk why
                self.analog['powerMeter']=temp[2]
                self.analog['rssi']=temp[3]
                self.analog['txPower']=temp[4]
                self.analog['elapsed']=round(elapsed,3)
                self.analog['timestamp']="%0.2f" % (time.time(),) 
                return self.analog
            else:
                return "No return error!"
        except Exception as error:
            print (error)
            pass

    """Function to receive a data packet from the board. Note: easier to use on threads"""
    def getDataInf(self, cmd):
        while True:
            try:
                start = time.clock()
                self.sendCMD(0,cmd,[])
                while True:
                    header = self.ser.read().decode('utf-8')
                    if header == '$':
                        header = header+self.ser.read(2).decode('utf-8')
                        break
                datalength = struct.unpack('<b', self.ser.read())[0]
                code = struct.unpack('<b', self.ser.read())
                data = self.ser.read(datalength)
                temp = struct.unpack('<'+'h'*int(datalength/2),data)
                elapsed = time.clock() - start
                self.ser.flushInput()
                self.ser.flushOutput()
                if cmd == DroneLib.ATTITUDE:
                    self.attitude['angx']=float(temp[0]/10.0)
                    self.attitude['angy']=float(temp[1]/10.0)
                    self.attitude['heading']=float(temp[2])
                    self.attitude['elapsed']="%0.3f" % (elapsed,)
                    self.attitude['timestamp']="%0.2f" % (time.time(),)
                elif cmd == DroneLib.RC:
                    self.rcChannels['roll']=temp[0]
                    self.rcChannels['pitch']=temp[1]
                    self.rcChannels['yaw']=temp[2]
                    self.rcChannels['throttle']=temp[3]
                    self.rcChannels['elapsed']="%0.3f" % (elapsed,)
                    self.rcChannels['timestamp']="%0.2f" % (time.time(),)
                elif cmd == DroneLib.RAW_IMU:
                    self.rawIMU['ax']=float(temp[0])
                    self.rawIMU['ay']=float(temp[1])
                    self.rawIMU['az']=float(temp[2])
                    self.rawIMU['gx']=float(temp[3])
                    self.rawIMU['gy']=float(temp[4])
                    self.rawIMU['gz']=float(temp[5])
                    self.rawIMU['elapsed']="%0.3f" % (elapsed,)
                    self.rawIMU['timestamp']="%0.2f" % (time.time(),)
                elif cmd == DroneLib.MOTOR:
                    self.motor['m1']=float(temp[0])
                    self.motor['m2']=float(temp[1])
                    self.motor['m3']=float(temp[2])
                    self.motor['m4']=float(temp[3])
                    self.motor['elapsed']="%0.3f" % (elapsed,)
                    self.motor['timestamp']="%0.2f" % (time.time(),)
            except Exception as error:
                print(error)
                pass

    """Function to ask for 2 fixed cmds, attitude and rc channels, and receive them. Note: is a bit slower than others"""
    def getData2cmd(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,self.ATTITUDE,[])
            while True:
                header = self.ser.read().decode('utf-8')
                if header == '$':
                    header = header+self.ser.read(2).decode('utf-8')
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp = struct.unpack('<'+'h'*int(datalength/2),data)
            self.ser.flushInput()
            self.ser.flushOutput()

            self.sendCMD(0,self.RC,[])
            while True:
                header = self.ser.read().decode('utf-8')
                if header == '$':
                    header = header+self.ser.read(2).decode('utf-8')
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp2 = struct.unpack('<'+'h'*int(datalength/2),data)
            elapsed = time.time() - start
            self.ser.flushInput()
            self.ser.flushOutput()

            if cmd == DroneLib.ATTITUDE:
                self.message['angx']=float(temp[0]/10.0)
                self.message['angy']=float(temp[1]/10.0)
                self.message['heading']=float(temp[2])
                self.message['roll']=temp2[0]
                self.message['pitch']=temp2[1]
                self.message['yaw']=temp2[2]
                self.message['throttle']=temp2[3]
                self.message['elapsed']=round(elapsed,3)
                self.message['timestamp']="%0.2f" % (time.time(),) 
                return self.message
            else:
                return "No return error!"
        except Exception as error:
            print (error)

    def reboot(self):
        self.sendCMD(0,self.REBOOT,[],'')
        self.ser.close()
        time.sleep(3)
        self.ser.open()