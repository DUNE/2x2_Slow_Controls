from app.CLASSES.UNIT_library import UNIT
from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import traceback
import sys
import threading
from configparser import ConfigParser

class MPOD(UNIT):
    '''
    This class represents the template for an MPOD.
    '''
    def __init__(self, module, unit, dict_unit, miblib='app/CONFIG/mibs_mpod'):
        '''
        Unit constructor
        '''
        self.miblib = miblib
        super().__init__(module, unit)
        self.dictionary = dict_unit
        self.module = module
        self.crate_status = self.getCrateStatus()
        self.measuring_status = self.getMeasuringStatus()
        
        # START CONTINUOUS MONITORING ON OBJECT CREATION
        if self.module != None:
            for powering in self.getPoweringList():
                for channel in self.getChannelList(powering):
                    threading.Thread(target=self.CONTINUOUS_monitoring, args=([[powering, channel, self.dictionary['powering'][powering]['channels'][channel]["name"]]]), kwargs={}).start()
                    time.sleep(1)

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
    
    def getMeasurementTemperature(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementTemperature" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        return ret[0].split(" ")[-2]

    def getMeasurementSenseVoltage(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel
        output = self.execute_command(command)
        ret = output.split('\n')        
        if ret and ret[0]:
            return ret[0].split(" ")[-2]
        else:
            raise ValueError("Failed to retrieve measurement sense voltage")
        
    def getMeasurementTerminalVoltage(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementTerminalVoltage" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        if ret and ret[0]:
            return ret[0].split(" ")[-2]
        else:
            raise ValueError("Failed to retrieve measurement terminal voltage")
        
    def getStatus(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputStatus" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        return ret
    
    def getMeasurementCurrent(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        return ret[0].split(" ")[-2]
    
    def getSysStatus(self):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysStatus.0" 
        output = self.execute_command(command)
        options = ['mainOn', 'mainInhibit', 'localControlOnly', 'inputFailure', 'outputFailure', 'fantrayFailure', 'sensorFailure', 'vmeSysfail', 'plugAndPlayIncompatible', 'busReset', 'supplyDerating', 'supplyFailure', 'supplyDerating2', 'supplyFailure2']
        for option in options:
            if option in output:
                return option
    
    def getCrateStatus(self):
        #return True
        '''
        Getting MPOD crate status
        '''
        command = "snmpget -v 2c -Oqv -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysMainSwitch.0"
        output = self.execute_command(command)
        status = True if "on" in output else False
        if status:
            self.crate_status = True # ON
        else:
            self.crate_status = False # OFF
            self.measuring_status = {key: False for key in self.dictionary['powering'].keys()}
        return status

    def getMeasuringStatus(self):
        '''
        Getting MPOD channels status
        '''
        try:
            if self.unit != "mpod_crate":
                self.measuring_status = {}
                for key in self.dictionary['powering'].keys():
                    self.measuring_status[key] = {}
                    for channel in self.dictionary['powering'][key]['channels'].keys():
                        data = self.measure([key, channel])
            else:
                self.measuring_status = None
            return self.measuring_status
        
        except Exception as e:
            print("Exception Found in Measuring Status: " + key + ", " + channel, e)
            self.error_status = True     
            self.measuring_status = None  
            return self.measuring_status

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # SET METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def setMaxCurrent(self, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputSupervisionMaxCurrent" + channel + " F " + str(I))

    def setCurrent(self, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputCurrent" + channel + " F " + str(I))

    def setMaxSenseVoltage(self, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip']+ " outputSupervisionMaxSenseVoltage" + channel + " F " + str(V))

    def setMaxVoltage(self, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputSupervisionMaxTerminalVoltage" + channel + " F " + str(V))

    def setVoltageRiseRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputVoltageRiseRate" + channel + " F " + str(rate))

    def setVoltage(self, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip']  + " outputVoltage" + channel + " F " + str(V))

    def setVoltageFallRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputVoltageFallRate" + channel + " F " + str(rate))

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def powerSwitch(self, switch):
        '''
        Powering ON/OFF power supply
        '''
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " sysMainSwitch" + ".0 i " + str(switch))
        if switch == 0:
            self.crate_status = False # OFF
            self.measuring_status = {key: False for key in self.dictionary['powering'].keys()}
        else:
            self.crate_status = True # ON
        time.sleep(2)

    def channelSwitch(self, switch, channel):
        '''
        Individual Channel Switch
        '''
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.dictionary['ip'] + " outputSwitch" + channel + " i " + str(switch))
        
    def powerON_channel(self, powering, channel):
        '''
        Power-ON single channel
        '''
        channels = self.getChannelDict(powering)
        selected_channel = channels[channel]
        self.setMaxCurrent(selected_channel['max_current'], channel)
        self.setCurrent(selected_channel['current_limit'], channel)
        self.setMaxSenseVoltage(selected_channel['max_sense_voltage'], channel)
        self.setMaxVoltage(selected_channel['max_terminal_voltage'], channel)
        # Ramping up voltage of channel
        self.setVoltageRiseRate(selected_channel['rate'], channel)
        self.channelSwitch(1, channel)
        self.setVoltage(selected_channel['sense_voltage'], channel)
        self.measuring_status[powering][channel] = True

    def powerOFF_channel(self, powering, channel):
        '''
        Power-OFF single channel
        '''
        channels = self.getChannelDict(powering)
        selected_channel = channels[channel]
        # Ramping down voltage of channel
        self.setVoltageFallRate(selected_channel['rate'], channel)
        self.setVoltage(selected_channel['sense_voltage'], channel)
        self.channelSwitch(0, channel)
        self.measuring_status[powering][channel] = False

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def measure(self, powering_array):
        '''
        Measures all channels in powering category
        '''
        Svalues, Status_message, V_sense_values, V_terminal_values, Ivalues = [], [], [], [], []
        V_sense_values_RMS, V_terminal_values_RMS, Ivalues_RMS = [], [], []
        powering, channel = powering_array[0], powering_array[1]

        # Measuring sense voltage, terminal voltage, and current
        V_terminal_values += [float(self.getMeasurementTerminalVoltage(channel))]
        V_sense_values += [float(self.getMeasurementSenseVoltage(channel))]
        Ivalues += [float(self.getMeasurementCurrent(channel))]

        # Measuring status
        status_answer = self.getStatus(channel)
        status = status_answer[0]
        Status_message = [status]

        # Catch all possible output messages and categorize them in ON/OFF/WARN/ERROR categories.
        if "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0)" in status:
            Svalues += ["ON"]
        elif "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00" in status:
            Svalues += ["OFF"]
        elif "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1)" in status:
            Svalues += ["WARN"]
        elif any(s in status for s in ["No Such Instance"]):
            Svalues += ["OFF"]
            Vvalues += ["0.000"]
            Ivalues += ["0.000"]
        elif any(s in status for s in ["Failure"]):
            Svalues += ["ERROR"]
        elif any(s in status for s in ["Limited", "Ramp", "EnableKill", "EmergencyOff", "Adjusting", "Constant", "Current"]):
            Svalues += ["WARN"]
        else:
            Svalues += [status_answer] 
            Status_message = [status_answer] 

        # Setting object status (this is for GUI, not influxDB)
        if Svalues[0]=="ON" or Svalues[0]=="WARN":
            self.measuring_status[powering][channel] = True 
        else:
            self.measuring_status[powering][channel] = False  

        # Initial RMS values (it's actually standard deviation, historical reasons...)
        V_sense_values_RMS += [0.000]      
        V_terminal_values_RMS += [0.000]   
        Ivalues_RMS += [0.000]   

        return Svalues,Status_message,V_sense_values,V_sense_values_RMS,V_terminal_values,V_terminal_values_RMS,Ivalues,Ivalues_RMS

    def write_log(self):
        powering_list = self.getPoweringList()
        f = open("Historical.log", "a")
        f.write(str(datetime.now()) + "\n")
        for powering in powering_list:
            channels = list(self.getChannelDict(powering).keys())
            log_data = self.measure(powering)
            for i in range(len(log_data[0])):
                f.write(str(channels[i]) +"\t"+ str(log_data[0][i]) + "\t" + str(log_data[1][i]) + " V \t" + str(log_data[2][i]) + " A\n")
        f.close()
    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, powering, channel_number, channel_name, data):
        '''
        Inputs:         - Powering (i.e. PACMAN&FANS)
                        - Channel number (i.e. .u100)
                        - Channel name (i.e. Mod0-TPC2_PACMAN)
                        - Data (measurement array)

        Description:    Record timestamp on InfluxDB
        '''
        client = self.InitializeInfluxDB()
        measurements_list = self.getMeasurementsList(powering)
        data = np.array(data)
        channel_temperature = self.getMeasurementTemperature(channel_number)
        if channel_temperature=='this':
            channel_temperature = None
        else:
            channel_temperature = float(channel_temperature)
        sys_status = self.getSysStatus()
        for i in range(0,data.shape[1]) :
            data_column = data[:,i]
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_number = channel_number,
                channel_name = channel_name,
                channel_temperature = channel_temperature,
                sys_status = sys_status,
                status_message = data_column[1],
                status = data_column[0],
                fields = zip(measurements_list, 
                             [float(element) for element in data_column[2:]])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_number, channel_name, channel_temperature, sys_status, status_message, status, fields):
            '''
            Inputs:         - Measurement (i.e. PACMAN&FANS)
                            - Channel name (i.e. .u100)
                            - Channel name (i.e. Mod0-TPC2_PACMAN)
                            - Status (i.e. OFF)
                            - Status message (i.e WIENER-CRATE-MIB::outputStatus ...)
                            - Fields (i.e. Voltages & current)

            Outputs:        - JSON file ready to be added to InfluxDB

            Description:    Provides new timestamp ready to be added to InfluxDB
            '''
            json_payload = []
            
            data = {
                # Table name
                "measurement" : measurement, 
                # Organization tags
                "tags" : { 
                    "channel_number" : channel_number,
                    "channel_name" : channel_name,
                    #"status" : status,
                    "status_message" : status_message
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            data["fields"]["channel_temperature"] = channel_temperature
            data["fields"]["status"] = status
            data["fields"]["status_message"] = status_message
            data["fields"]["channel_name"] = channel_name
            data["fields"]["system_status"] = sys_status
            json_payload.append(data)
            return json_payload
    
    def CONTINUOUS_monitoring(self, powering_array):
        '''
        Inputs:         - Powering (i.e. [PACMAN&FANS, .u100, Mod0-TPC2_PACMAN])

        Description:    Continuously record timestamp on InfluxDB only if MPOD crate is powered.
        '''
        powering, channel_number, channel_name = powering_array[0], powering_array[1], powering_array[2]
        if self.getCrateStatus():
            print("MPOD Continuous DAQ Activated: " + str(self.module) + ", " + powering + ", " + channel_number+ ". Taking data in real time")
        measurements_list = self.getMeasurementsList(powering)

        # Run monitoring
        while True:
            
            try:
                if self.getCrateStatus():
                    # Creating dict for data 
                    sampled_values = {}  
                    for measurement in measurements_list:
                        sampled_values[measurement] = [] 

                    # Record data for 5 seconds
                    elapsed_time = 0
                    start_time = time.time()
                    while elapsed_time < 10:
                        time.sleep(2)
                        measurement_values = self.measure(powering_array)[2:]
                        for index, measurement in enumerate(measurements_list):
                            sampled_values[measurement].append(measurement_values[index])
                        elapsed_time = time.time() - start_time

                    # Make array of mean and RMS values
                    data = np.array(self.measure(powering_array))
                    filtered_list = [element for element in measurements_list if "_STD" not in element]
                    for index, measurement in enumerate(filtered_list): 
                        mean = np.mean(sampled_values[measurement])
                        STD = np.std(sampled_values[measurement])
                        data[2*index+2] = str(mean) 
                        data[2*index+3] = str(STD) 
                    # Push data to InfluxDB
                    self.INFLUX_write(powering,channel_number,channel_name,data)

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                print(powering)
                traceback.print_exc()
            
