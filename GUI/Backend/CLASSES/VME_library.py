from app.CLASSES.UNIT_library import UNIT
from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import traceback
import threading
import sys
import re
import subprocess

class VME(UNIT):
    '''
    This class represents the template for a VME.
    '''
    def __init__(self, module, unit, dict_unit, miblib='app/CONFIG/mibs_vme'):
        '''
        Unit constructor
        '''
        self.miblib = miblib
        super().__init__(module, unit)
        self.dictionary = dict_unit
        self.crate_status = self.getCrateStatus()
        self.measuring_status = self.getMeasuringStatus()

        # START CONTINUOUS MONITORING ON OBJECT CREATION
        for powering in self.getPoweringList():
            for channel in self.getChannelList(powering):
                threading.Thread(target=self.CONTINUOUS_monitoring, args=([[powering, channel, self.dictionary['powering'][powering]['channels'][channel]["name"]]]), kwargs={}).start()


    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    #def vmeSwitch(self, vmen, switch):
    #    os.popen("snmpset -v 2c -M " + str(self.miblib) + " -m +WIENER-CRATE-MIB -c guru " + str(self.ip[vmen]) + " sysMainSwitch.0 i " + str(switch))
        #os.popen("snmpset -v 2c -M ./mibs -m +WIENER-CRATE-MIB -c guru " + self.ip[0] + " sysMainSwitch.0 i " + str(switch))

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # GET METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#--- 

    def getCrateStatus(self): 
        #return True           
        #command = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysMainSwitch" + ".0")
        #command.close()
        #output_file = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysMainSwitch" + ".0")
        #output = output_file.read()
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysMainSwitch" + ".0"
        output = self.execute_command(command)
        status = True if "on(1)" in output else False
        #output_file.close()
        return status 

    def getPoweringList(self):
        return self.dictionary['powering'].keys()    

    def getChannelList(self, powering):
        return self.dictionary['powering'][powering]['channels'].keys()  
    
    def getMeasurementsList(self, powering):
        return self.dictionary['powering'][powering]['measurements']

    def getMeasuringStatus(self):
        try:
            self.measuring_status = {}
            for key in self.dictionary['powering'].keys():
                self.measuring_status[key] = {}
                for channel in self.dictionary['powering'][key]['channels'].keys():
                    data = self.measure([key, channel])
            return self.measuring_status
        
        except Exception as e:
            print("Exception Found in Measuring Status: " + key + ", " + channel, e)
            self.error_status = True     
            self.measuring_status = None  
            return self.measuring_status

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def getTemperature(self, sensor):
        '''
        Returns the Temperature of the sensor 
        ''' 
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sensorTemperature" + sensor)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sensorTemperature" + sensor
        output = self.execute_command(command)
        #command = "snmpget -v 2c -M {} -m +WIENER-CRATE-MIB -c public {} sensorTemperature {}".format(self.miblib, self.dictionary['ip'], sensor)
        #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        #output, _ = process.communicate()
        #ret = output.decode().split('\n')
        ret = output.split('\n')
        #ret = data.read().split('\n')
        #data.close()
        return float(ret[0].split(" ")[-2])
    
    def getMeasurementSenseVoltage(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        #ret = data.read().split('\n')
        #data.close()
        if ret and ret[0]:
            return ret[0].split(" ")[-2]
        else:
            raise ValueError("Failed to retrieve measurement sense voltage")
        
    def getMeasurementTerminalVoltage(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputSupervisionMaxTerminalVoltage" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputSupervisionMaxTerminalVoltage" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        #ret = data.read().split('\n')
        #data.close()
        if ret and ret[0]:
            return ret[0].split(" ")[-2]
        else:
            raise ValueError("Failed to retrieve measurement terminal voltage")
        
    def getMeasurementCurrent(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel
        output = self.execute_command(command)
        ret = output.split('\n')
        #ret = data.read().split('\n')
        #data.close()
        return ret[0].split(" ")[-2]
    
    def measure(self, powering_array):
        '''
        Measures all channels in powering category
        '''
        #Svalues, Status_message, V_sense_values, V_terminal_values, Ivalues = [], [], [], [], []
        #V_sense_values_RMS, V_terminal_values_RMS, Ivalues_RMS = [], [], []
        powering, channel = powering_array[0], powering_array[1]
        # Measuring sense voltage, terminal voltage, and current
        if powering == "electrical_params":
            V_sense_values, V_terminal_values, Ivalues = [], [], []
            V_sense_values_RMS, V_terminal_values_RMS, Ivalues_RMS = [], [], []
            V_terminal_values += [float(self.getMeasurementTerminalVoltage(channel))]
            V_sense_values += [float(self.getMeasurementSenseVoltage(channel))]
            Ivalues += [float(self.getMeasurementCurrent(channel))]
            V_sense_values_RMS += [0.000]      
            V_terminal_values_RMS += [0.000]   
            Ivalues_RMS += [0.000]   
            return V_terminal_values, V_terminal_values_RMS, V_sense_values, V_sense_values_RMS, Ivalues, Ivalues_RMS
            
        elif powering == "temperature":
            temperature_value_RMS, temperature_value = [], []
            temperature_value += [self.getTemperature(channel)]
            temperature_value_RMS += [0.000]  
            return temperature_value, temperature_value_RMS
        
        # Measuring crate status
        #self.measuring_status[powering][channel] = True 

        # Measuring sense voltage, terminal voltage, and current
        #V_terminal_values += [float(self.getMeasurementTerminalVoltage(channel))]
        #V_sense_values += [float(self.getMeasurementSenseVoltage(channel))]
        #Ivalues += [float(self.getMeasurementCurrent(channel))]

        # Measuring status
        #status = self.getStatus(channel)[0]
        #Status_message = [status]
        #if status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0) ":
        #    Svalues += ["ON"]
        #elif status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00 ":
        #    Svalues += ["OFF"]
        #elif status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1) ":
        #    Svalues += ["ILOCK"]
        #elif any(s in status for s in ["No Such Instance"]):
        #    Svalues += ["OFF"]
        #    Vvalues += ["0.000"]
        #    Ivalues += ["0.000"]
        #elif any(s in status for s in ["Limited", "Failure"]):
            #Svalues += ["OFF"]
        #    Svalues += ["WARN"]
        #else:
        #    Svalues += [self.getStatus(channel)] 
        #    Status_message = [self.getStatus(channel)] 

        # Setting object status (this is for GUI, not influxDB)
        #if Svalues[0]=="ON" or Svalues[0]=="WARN":
        #    self.measuring_status[powering][channel] = True 
        #else:
        #    self.measuring_status[powering][channel] = False  

        return temperature_value, temperature_value_RMS

    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, powering, channel_number, channel_name, data):
        '''
        Inputs:         - Powering (i.e. temperatures)
                        - Channel number (i.e. .temp1)
                        - Channel name (i.e. sensor1)
                        - Data (measurement array)

        Description:    Record timestamp on InfluxDB
        '''
        client = self.InitializeInfluxDB()
        measurements_list = self.getMeasurementsList(powering)
        data = np.array(data)
        for i in range(0,data.shape[1]) :
            data_column = data[:,i]
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_number = channel_number,
                channel_name = channel_name,
                fields = zip(measurements_list, 
                             [float(element) for element in data_column])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_number, channel_name, fields):
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
                    #"status_message" : status_message
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            data["fields"]["crate_status"] = self.getCrateStatus()
            json_payload.append(data)
            return json_payload
    
    def CONTINUOUS_monitoring(self, powering_array):
        '''
        Inputs:         - Powering (i.e. [PACMAN&FANS, .u100, Mod0-TPC2_PACMAN])

        Description:    Continuously record timestamp on InfluxDB only if MPOD crate is powered.
        '''
        powering, channel_number, channel_name = powering_array[0], powering_array[1], powering_array[2]
        if self.getCrateStatus():
            print("VME Continuous DAQ Activated: " + powering + ", " + channel_number+ ". Taking data in real time")
        measurements_list = self.getMeasurementsList(powering)

        # Run monitoring 
        while True:
            if self.getCrateStatus():
                try:
                    # Creating dict for data 
                    sampled_values = {}  
                    for measurement in measurements_list:
                        sampled_values[measurement] = [] 

                    # Record data for 5 seconds
                    elapsed_time = 0
                    start_time = time.time()
                    while elapsed_time < 10:
                        measurement_values = self.measure(powering_array)
                        for index, measurement in enumerate(measurements_list):
                            sampled_values[measurement].append(measurement_values[index])
                        elapsed_time = time.time() - start_time

                    # Make array of mean and RMS values
                    data = np.array(self.measure(powering_array))
                    filtered_list = [element for element in measurements_list if "_STD" not in element]
                    for index, measurement in enumerate(filtered_list): 
                        mean = np.mean(sampled_values[measurement])
                        STD = np.std(sampled_values[measurement])
                        data[2*index] = str(mean) 
                        data[2*index+1] = str(STD) 
                    # Push data to InfluxDB
                    self.INFLUX_write(powering,channel_number,channel_name,data)

                except Exception as e:
                    print('*** Caught exception: %s: %s' % (e.__class__, e))
                    print(powering)
                    traceback.print_exc()