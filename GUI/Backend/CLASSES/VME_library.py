from app.CLASSES.UNIT_library import UNIT
from pysnmp.hlapi import *
import time 
from datetime import datetime
import numpy as np
import traceback
import threading
import os

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
                time.sleep(1)


    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    #def vmeSwitch(self, vmen, switch):
    #    os.popen("snmpset -v 2c -M " + str(self.miblib) + " -m +WIENER-CRATE-MIB -c guru " + str(self.ip[vmen]) + " sysMainSwitch.0 i " + str(switch))
        #os.popen("snmpset -v 2c -M ./mibs -m +WIENER-CRATE-MIB -c guru " + self.ip[0] + " sysMainSwitch.0 i " + str(switch))

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
    def getStatus(self, channel):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputStatus" + channel
        try:
            output = self.execute_command(command)
            ret = output.split('\n')
        except AttributeError as e:
            return None
        return ret
    
    def getTemperature(self, sensor):
        '''
        Returns the Temperature of the sensor 
        ''' 
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sensorTemperature" + sensor)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sensorTemperature" + sensor
        try:
            output = self.execute_command(command)
            ret = output.split('\n')
        except AttributeError as e:
            return None
        #command = "snmpget -v 2c -M {} -m +WIENER-CRATE-MIB -c public {} sensorTemperature {}".format(self.miblib, self.dictionary['ip'], sensor)
        #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        #output, _ = process.communicate()
        #ret = output.decode().split('\n')
        #ret = data.read().split('\n')
        #data.close()
        return float(ret[0].split(" ")[-2])
    
    def getMeasurementSenseVoltage(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel
        try:
            output = self.execute_command(command)
            ret = output.split('\n')
        except AttributeError as e:
            return None
        #ret = data.read().split('\n')
        #data.close()
        if ret and ret[0]:
            return float(ret[0].split(" ")[-2])
        else:
            raise ValueError("Failed to retrieve measurement sense voltage")
        
    def getMeasurementTerminalVoltage(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputSupervisionMaxTerminalVoltage" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputSupervisionMaxTerminalVoltage" + channel
        try:
            output = self.execute_command(command)
            ret = output.split('\n')
        except AttributeError as e:
            return None
        #ret = data.read().split('\n')
        #data.close()
        if ret and ret[0]:
            return float(ret[0].split(" ")[-2])
        else:
            raise ValueError("Failed to retrieve measurement terminal voltage")
        
    def getMeasurementCurrent(self, channel):
        #data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel)
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel
        try:
            output = self.execute_command(command)
            ret = output.split('\n')
        except AttributeError as e:
            return None
        #ret = data.read().split('\n')
        #data.close()
        return float(ret[0].split(" ")[-2])
    
    def getSysStatus(self):
        command = "snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " sysStatus.0" 
        output = self.execute_command(command)
        options = ['mainOn', 'mainInhibit', 'localControlOnly', 'inputFailure', 'outputFailure', 'fantrayFailure', 'sensorFailure', 'vmeSysfail', 'plugAndPlayIncompatible', 'busReset', 'supplyDerating', 'supplyFailure', 'supplyDerating2', 'supplyFailure2']
        for option in options:
            if option in output:
                return option
            
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    
    def measure(self, powering_array):
        '''
        Measures all channels in powering category
        '''
        #Svalues, Status_message, V_sense_values, V_terminal_values, Ivalues = [], [], [], [], []
        #V_sense_values_RMS, V_terminal_values_RMS, Ivalues_RMS = [], [], []
        powering, channel = powering_array[0], powering_array[1]
        Svalues, Status_message = [], []
        # Measuring sense voltage, terminal voltage, and current
        if powering == "electrical_params":
            V_sense_values, V_terminal_values, Ivalues = [], [], []
            V_sense_values_RMS, V_terminal_values_RMS, Ivalues_RMS = [], [], []
            V_terminal_values += [self.getMeasurementTerminalVoltage(channel)]
            V_sense_values += [self.getMeasurementSenseVoltage(channel)]
            Ivalues += [self.getMeasurementCurrent(channel)]
            V_sense_values_RMS += [0.000]      
            V_terminal_values_RMS += [0.000]   
            Ivalues_RMS += [0.000]

            # Measuring status
            status_answer = self.getStatus(channel)
            status = status_answer[0]
            Status_message = [status]
            if "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0)" in status:
                Svalues += ["ON"]
            elif "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00" in status:
                Svalues += ["OFF"]
            elif "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1)" in status:
                Svalues += ["ILOCK"]
            elif any(s in status for s in ["No Such Instance"]):
                Svalues += ["OFF"]
                Vvalues += ["0.000"]
                Ivalues += ["0.000"]
            elif any(s in status for s in ["Limited", "Failure"]):
                #Svalues += ["OFF"]
                Svalues += ["WARN"]
            else:
                Svalues += [status_answer] 
                Status_message = [status_answer] 

            return Svalues,Status_message,V_terminal_values, V_terminal_values_RMS, V_sense_values, V_sense_values_RMS, Ivalues, Ivalues_RMS
            
        elif powering == "temperature":
            temperature_value_RMS, temperature_value = [], []
            temperature_value += [self.getTemperature(channel)]
            temperature_value_RMS += [0.000]  
            if temperature_value[0] > 0:
                Svalues += ["ON"]
                Status_message = ["Sensor is operational."] 
            else:
                Svalues += ["OFF"]
                Status_message = ["Nothing"] 
            return Svalues,Status_message,temperature_value, temperature_value_RMS
        
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
        sys_status = self.getSysStatus()
        for i in range(0,data.shape[1]) :
            data_column = data[:,i]
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_number = channel_number,
                channel_name = channel_name,
                sys_status = sys_status,
                status_message = data_column[1],
                status = data_column[0],
                fields = zip(measurements_list, 
                             [float(element) for element in data_column[2:]])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_number, channel_name, sys_status, status_message, status, fields):
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
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            data["fields"]["status"] = status
            # Assigning values to error messages
            if status == "OFF":
                status_number = 0
            elif status == "ON":
                status_number = 1
            elif status == "WARN":
                status_number = 2
            elif status == "ERROR":
                status_number = 3
            data["fields"]["status_number"] = status_number
            data["fields"]["status_message"] = status_message
            data["fields"]["channel_name"] = channel_name
            data["fields"]["system_status"] = sys_status
            data["fields"]["crate_status"] = self.crate_status
            json_payload.append(data)
            return json_payload
    
    def CONTINUOUS_monitoring(self, powering_array):
        '''
        Inputs:         - Powering (i.e. [PACMAN&FANS, .u100, Mod0-TPC2_PACMAN])

        Description:    Continuously record timestamp on InfluxDB only if MPOD crate is powered.
        '''
        powering, channel_number, channel_name = powering_array[0], powering_array[1], powering_array[2]
        print("VME Continuous DAQ Activated: " + powering + ", " + channel_number+ ". Taking data in real time")
        measurements_list = self.getMeasurementsList(powering)

        # Run monitoring 
        while True:

            try:
                # Creating dict for data 
                sampled_values = {}  
                for measurement in measurements_list:
                    sampled_values[measurement] = [] 

                # Record data for 10 seconds
                self.crate_status = self.getCrateStatus()
                elapsed_time = 0
                start_time = time.time()
                while elapsed_time < 10:
                    time.sleep(2)
                    measurement_values = self.measure(powering_array)[2:]
                    for index, measurement in enumerate(measurements_list):
                        sampled_values[measurement].append(measurement_values[index])
                    elapsed_time = time.time() - start_time
                
                # Make array of mean and STD values
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