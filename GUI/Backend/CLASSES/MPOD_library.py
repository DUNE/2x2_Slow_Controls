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
        if self.crate_status and self.module != None:
            for powering in self.getPoweringList():
                for channel in self.getChannelList(powering):
                    threading.Thread(target=self.CONTINUOUS_monitoring, args=([[powering, channel, self.dictionary['powering'][powering]['channels'][channel]["name"]]]), kwargs={}).start()


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
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementTemperature" + channel)
        ret = data.read().split('\n')
        return ret[0].split(" ")[-2]

    def getMeasurementSenseVoltage(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel)
        ret = data.read().split('\n')
        if ret and ret[0]:
            return ret[0].split(" ")[-2]
        else:
            raise ValueError("Failed to retrieve measurement sense voltage")
        
    def getStatus(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputStatus" + channel)  
        #return data.read().split('= ')[1].split('\n')[0]
        return data.read().split('\n')
    
    def getMeasurementCurrent(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel)
        ret = data.read().split('\n')
        return ret[0].split(" ")[-2]
    
    def getCrateStatus(self):
        #return True
        first_channel = next(iter(self.getChannelList('PACMAN&FANS')))
        try:
            return False if  "No Such Instance" in self.measure(['PACMAN&FANS',first_channel])[0][0][0] else True
        except Exception as e:
            print("Exception Found Getting Crate Status: ", e)
            self.error_status = True
            return True

    def getMeasuringStatus(self):
        '''
        return { # TEST OUTPUT FOR MOD0
            "PACMAN&FANS" : {
                ".u0" : False,
                ".u1" : False,
                ".u100" : False,
                ".u101" : False,
                ".u102" : False
            },
            "VGAs" : {
                ".u300" : False,
                ".u301" : False,
                ".u302" : False,
                ".u303" : False
            },
            "RTDs" : {
                ".u200" : False,
                ".u201" : False
            }
        }
        '''
        try:
            if self.unit != "mpod_crate":
                self.measuring_status = {}
                for key in self.dictionary['powering'].keys():
                    self.measuring_status[key] = {}
                    for channel in self.dictionary['powering'][key]['channels'].keys():
                        data = self.measure([key, channel])
                        if self.measure([key, channel])[0][0]=="ON":
                            self.measuring_status[key][channel] = True 
                        #elif self.measure([key, channel])[0][0]=="OFF":
                        else:
                            self.measuring_status[key][channel] = False
                        #elif any(s in data[0][0][0] for s in ["No Such Instance"]):
                        #    self.measuring_status[key][channel] = False
                        #elif any(s in data[0][0][0] for s in ["BITS"]):
                        #    self.measuring_status[key][channel] = True 
                        #elif any(s in data[0][0][0] for s in ["Limited", "Failure"]):
                        #    self.measuring_status[key][channel] = False
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
            self.crate_status = False # ON
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
        Svalues, Vvalues, Ivalues = [], [], []
        powering, channel = powering_array[0], powering_array[1]

        # Measuring voltage and current
        Vvalues += [self.getMeasurementSenseVoltage(channel)]
        Ivalues += [self.getMeasurementCurrent(channel)]

        # Measuring status
        status = self.getStatus(channel)[0]
        if status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0) ":
            Svalues += ["ON"]
        elif status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00 ":
            Svalues += ["OFF"]
        elif status == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1) ":
            Svalues += ["ILOCK"]
        elif any(s in status for s in ["No Such Instance"]):
            Svalues += ["OFF"]
            Vvalues += ["0.000"]
            Ivalues += ["0.000"]
        elif any(s in status for s in ["BITS"]):
            Svalues += ["ON"]
        elif any(s in status for s in ["Limited", "Failure"]):
            Svalues += ["OFF"]
        else:
            Svalues += [self.getStatus(channel)]            
    
        return Svalues,Vvalues,Ivalues

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
        for i in range(0,data.shape[1]) :
            data_column = data[:,i]
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_number = channel_number,
                channel_name = channel_name,
                channel_temperature = channel_temperature,
                status = data_column[0],
                fields = zip(measurements_list, 
                             [float(element) for element in data_column[1:]])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_number, channel_name, channel_temperature, status, fields):
            '''
            Inputs:         - Measurement (i.e. PACMAN&FANS)
                            - Channel name (i.e. .u100)
                            - Channel name (i.e. Mod0-TPC2_PACMAN)
                            - Status (i.e. OFF)
                            - Fields (i.e. Voltage & current)

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
                    "status" : status
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            data["fields"]["channel_temperature"] = channel_temperature
            json_payload.append(data)
            return json_payload
    
    def CONTINUOUS_monitoring(self, powering_array):
        '''
        Inputs:         - Powering (i.e. [PACMAN&FANS, .u100, Mod0-TPC2_PACMAN])

        Description:    Continuously record timestamp on InfluxDB
        '''
        powering, channel_number, channel_name = powering_array[0], powering_array[1], powering_array[2]
        try:
            print("MPOD Continuous DAQ Activated: " + str(self.module) + ", " + powering + ", " + channel_number+ ". Taking data in real time")
            while self.getCrateStatus():
                data = self.measure(powering_array)
                self.INFLUX_write(powering,channel_number,channel_name,data)
                time.sleep(2)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)