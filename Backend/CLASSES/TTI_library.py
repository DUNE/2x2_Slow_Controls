from app.CLASSES.UNIT_library import UNIT
import socket
from datetime import datetime
import time 
import traceback
import sys

class TTI(UNIT):
    '''
    This class represents the template for a TTI.
    '''
    def __init__(self, module, unit, dict_unit):
        super().__init__(module, unit)
        self.dictionary = dict_unit
        self.crate_status = self.getCrateStatus() 
        self.packet_end = bytes('\r\n','ascii')
        self.measuring_status = self.getMeasuringStatus()
        self.ident_string = ''

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # GET METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def getOnMessage(self):
        return self.dictionary["on_message"]
    
    def getModules(self):
        return self.dictionary["modules"].keys()
    
    def getClass(self):
        return self.dictionary["class"]
    
    def getOffMessage(self):
        return self.dictionary["off_message"]

    def getIP(self):
        return self.dictionary['ip']
    
    def getPoweringList(self):
        return self.dictionary['powering'].keys()

    def getMeasurementsList(self, powering):
        return self.dictionary['powering'][powering]['measurements']
    
    def getChannelList(self, powering):
        return self.dictionary['powering'][powering]['channels'].keys()
    
    def getChannelDict(self, powering):
        return self.dictionary['powering'][powering]['channels']
    
    def getCrateStatus(self):
        try:
            self.readOutputVolts(1)
            self.crate_status = True
            return True
        except:
            self.crate_status = False
            return False
    
    def getMeasuringStatus(self):
        self.measuring_status = {}
        for key in self.dictionary['powering'].keys():
            channels = self.getChannelDict(key)
            try:
                if self.getOutputIsEnabled(list(channels)[0]):
                    self.measuring_status[key] = True 
                else:
                    self.measuring_status[key] = False
            except:
                self.measuring_status[key] = False
        return self.measuring_status
    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # PRE-DEFINED CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def recv_end(self, the_socket):
        total_data=[]
        data=''
        while True:
            data=the_socket.recv(1024)
            if self.packet_end in data:
                total_data.append(data[:data.find(self.packet_end)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if self.packet_end in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(self.packet_end)]
                    total_data.pop()
                    break
        return b''.join(total_data)
    
    # Sends and recieves a string
    def send_receive_string(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.dictionary["sock_timeout_secs"])
            s.connect((self.dictionary["ip"], self.dictionary["port"]))
            s.sendall(bytes(cmd,'ascii'))
            s.sendall(bytes(cmd,'ascii'))
            data = self.recv_end(s)
        return data.decode('ascii')
    
    # Sends and recieves a float
    def send_receive_float(self, cmd):
        r = self.send_receive_string(cmd)
        #Eg. '-0.007V\r\n'  '31.500\r\n'  'V2 3.140\r\n'
        r=r.rstrip('\r\nVA') #Strip these trailing chars
        l=r.rsplit() #Split to array of strings
        if len(l) > 0:
            return float(l[-1]) #Convert number in last string to float
        return 0.0
    
    # Reads output voltage
    def readOutputVolts(self, channel):
        cmd = 'V{}O?'.format(channel)
        v = self.send_receive_float(cmd)
        return v
    
    # Sends and recieves an integer
    def send_receive_integer(self, cmd):
        r = self.send_receive_string(cmd)
        return int(r)
    
    # Sends and recieves a boolean
    def send_receive_boolean(self, cmd):
        if self.send_receive_integer(cmd) > 0:
            return True
        return False

    # Tell me if the output is enabled
    def getOutputIsEnabled(self, channel):
        cmd = 'OP{}?'.format(channel)
        return self.send_receive_boolean(cmd)
    
    # Sets Output to be either on/off
    def setOutputEnable(self, ON, channel):
        cmd=''
        if ON == True:
            cmd = 'OP{} 1'.format(channel)
            self.measuring_status['voltage'] = True
        else:
            cmd = 'OP{} 0'.format(channel)
            self.measuring_status['voltage'] = False
        self.send(cmd)

    # Set current limit of output
    def setMaxAmps(self, amps, channel):
        cmd = 'I{0} {1:1.3f}'.format(channel, amps)
        self.send(cmd)

    # Set over current protection trip point
    def setTripAmps(self, amps, channel):
        cmd = 'OCP{0} {1:1.3f}'.format(channel, amps)
        self.send(cmd)

    # Set over voltage protection trip point
    def setTripVolts(self, volts, channel):
        cmd = 'OVP{} {}'.format(channel, volts)
        self.send(cmd)

    # Sets the voltage step size
    def setStepSizeVolts(self, step, channel):
        cmd = 'DELTAV{0} {1:1.3f}'.format(channel, step)
        self.send(cmd)

    # Set output voltage
    def setMaxVolts(self, volts, channel):
        cmd = 'V{0} {1:1.3f}'.format(channel, volts)
        self.send(cmd)

    # Communication command
    def send(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.dictionary["sock_timeout_secs"])
            s.connect((self.dictionary["ip"], self.dictionary["port"]))
            s.sendall(bytes(cmd,'ascii'))

    # Voltage command
    # Increments voltage
    def incrementVoltage(self, channel):
        cmd = 'INCV{}'.format(channel)
        self.send(cmd)

    # Decrements the voltage
    def decrementVoltage(self, channel):
        cmd = 'DECV{}'.format(channel)
        self.send(cmd)
    
    def ramp_up(self,V0,channel):
        status = True

        #   Makes sure output is turned off 
        try:
            self.setOutputEnable(False, channel)
        except:
            #failure(ip)
            return False
        
        #   Turns output on
        try:
            self.setOutputEnable(True, channel)
        except:
            #failure(ip)
            return False
        
        #	Test to ensure we can read voltages
        #try:
        #    print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
        #except:
            #failure(ip)
        #    return False
        
        #   Sets max current to 7.5 mA
        self.setMaxAmps(self.dictionary["powering"]["voltage"]["channels"]["1"]["max_current"], channel)
        self.setTripAmps(self.dictionary["powering"]["voltage"]["channels"]["1"]["tripAmps"], channel)
        self.setTripVolts(self.dictionary["powering"]["voltage"]["channels"]["1"]["tripVolts"], channel)
        #   Sets voltage step size
        self.setStepSizeVolts(self.dictionary["powering"]["voltage"]["channels"]["1"]["stepSizeVolts"], channel)
        #   Begins ramping up voltage
        if V0 > 6:
            #print("Starting Ramp")
            #   Slow at the beginning
            while self.readOutputVolts(channel) < 6:
                #   Stops if incrimentation fails
                try:
                    self.incrementVoltage(channel)
                    #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
                    #write()
                except:
                    #failure(ip)
                    status = False
                    break
                    
            #   Breaks ends the function if there was an issue in incrimentation
            if status == False:
                #failure(ip)
                return False
            
            #   Speeds up incrimentation
            fast_step = 6
            self.setStepSizeVolts(fast_step, channel)
            
            #   Same as above but now to V0
            while self.readOutputVolts(channel) < V0-fast_step:
                    try:    
                        self.incrementVoltage(channel)
                        #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
                        #write()
                    except:
                        #failure(ip)
                        status = False
                        break
                    if status == False:
                        #failure(ip)
                        return False
            
            self.setMaxVolts(channel, V0)
            #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")

        #   If voltage is lower than threshold to speed up then just do normally
        elif V0 < 7: 
            while self.readOutputVolts(channel) < 7:
                try:
                    self.incrementVoltage(channel)
                    #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
                except: 
                    #failure(ip)
                    break

        self.setStepSizeVolts(0, channel)
        self.setMaxVolts(channel, V0)            
        return True
    
    def ramp_down(self, channel):
            
        #   Prints the voltage it starts at
        #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
        #write() 
        #   initializes the voltage step size to 1
        self.setStepSizeVolts(6, channel)
        
        #   Lowers the voltage (reverse of before)
        while self.readOutputVolts(channel) > 0.1:
            if self.readOutputVolts(channel) < 7:
                try:
                    self.setStepSizeVolts(1, channel)
                except:
                #    failure(ip)
                    print("Error ramping down")        
            try:
                self.decrementVoltage(channel)
                #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
            except:
                #failure(ip)
                print("Error ramping down")  
            
        #   Sets voltage to zero and turns off output
        self.setMaxVolts(channel, 0)
        #print("The current Voltage is: " ,self.readOutputVolts(channel) ,"V")
        self.setOutputEnable(False, channel)

    def powerON(self, powering):
        '''
        Power-ON all channels
        '''
        channels = self.getChannelDict(powering)
        for channel in channels.keys():
            selected_channel = channels[channel]
            self.setOutputEnable(True, selected_channel)
            #self.ramp_up(1)

    def powerOFF(self, powering):
        '''
        Power-ON all channels
        '''
        channels = self.getChannelDict(powering)
        for channel in channels.keys():
            selected_channel = channels[channel]
            self.ramp_down(1)
            self.setOutputEnable(False, selected_channel)
   
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, powering, data):
        '''
        Inputs:         - Powering (i.e. voltage)
                        - Data (measurement array)

        Description:    Record timestamp on InfluxDB
        '''
        client = self.InitializeInfluxDB()
        channels = self.getChannelDict(powering)
        measurements_list = self.getMeasurementsList(powering)
        keys = list(channels.keys())
        for key in keys:
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_name = channels[key]["name"],
                fields = zip(measurements_list, [data])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_name, fields):
            '''
            Inputs:         - Measurement (i.e. voltage)
                            - Channel name (i.e. 1)
                            - Fields (i.e. Voltage)

            Outputs:        - JSON file ready to be added to InfluxDB

            Description:    Provides new timestamp ready to be added to InfluxDB
            '''
            json_payload = []
            data = {
                # Table name
                "measurement" : measurement, 
                # Organization tags
                "tags" : { 
                    "channel_name" : channel_name,
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            json_payload.append(data)
            return json_payload
    
    def CONTINUOUS_monitoring(self, powering):
        '''
        Inputs:         - Powering (i.e. voltage)

        Description:    Continuously record timestamp on InfluxDB
        '''
        try:
            print("Continuous DAQ Activated: " + powering + ". Taking data in real time")
            while self.getCrateStatus():
                data = self.readOutputVolts(1)
                self.INFLUX_write(powering,data)
                #self.write_log()
                time.sleep(2)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)