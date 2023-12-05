from app.CLASSES.UNIT_library import UNIT
from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import traceback
import sys
from configparser import ConfigParser

class MPOD(UNIT):
    '''
    This class represents the template for an MPOD.
    '''
    def __init__(self, module, unit, dict_unit, miblib='CONFIG/mibs/'):
        '''
        Unit constructor
        '''
        self.miblib = miblib
        super().__init__(module, unit)
        self.dictionary = dict_unit
        self.crate_status = self.getCrateStatus()
        self.measuring_status = self.getMeasuringStatus()

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

    def getMeasurementSenseVoltage(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementSenseVoltage" + channel)
        ret = data.read().split('\n')
        return ret[0].split(" ")[-2]
    
    def getStatus(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputStatus" + channel)  
        #return data.read().split('= ')[1].split('\n')[0]
        return data.read().split('\n')
    
    def getMeasurementCurrent(self, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.dictionary['ip'] + " outputMeasurementCurrent" + channel)
        ret = data.read().split('\n')
        return ret[0].split(" ")[-2]
    
    def getCrateStatus(self):
        return False if  "No Such Instance" in self.measure('charge')[0][0][0] else True
    
    def getMeasuringStatus(self):
        if self.unit != "mpod_crate":
            self.measuring_status = {}
            for key in self.dictionary['powering'].keys():
                if self.measure(key)[0][0]=="ON":
                    self.measuring_status[key] = True 
                else:
                    self.measuring_status[key] = False
        else:
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

    def powerON(self, powering):
        '''
        Power-ON all channels
        '''
        channels = self.getChannelDict(powering)
        for channel in channels.keys():
            selected_channel = channels[channel]
            self.setMaxCurrent(selected_channel['max_current'], channel)
            self.setCurrent(selected_channel['current'], channel)
            self.setMaxSenseVoltage(selected_channel['max_sense_voltage'], channel)
            self.setMaxVoltage(selected_channel['max_voltage'], channel)
            # Ramping up voltage of channel
            self.setVoltageRiseRate(selected_channel['rate'], channel)
            self.channelSwitch(1, channel)
            self.setVoltage(selected_channel['V'], channel)
            #print(str(channel), str(self.getMeasurementSenseVoltage(channel)), selected_channel['V'])
        self.measuring_status[powering] = True
        
    def powerOFF(self, powering):
        '''
        Power-OFF all channels
        '''
        channels = self.getChannelDict(powering)
        for channel in channels.keys():
            selected_channel = channels[channel]
            # Ramping down voltage of channel
            self.setVoltageFallRate(selected_channel['rate'], channel)
            self.setVoltage(selected_channel['V'], channel)
            #print(str(channel), str(self.getMeasurementSenseVoltage(channel)), selected_channel['V'])
            self.channelSwitch(0, channel)
        self.measuring_status[powering] = False

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def measure(self, powering):
        Svalues, Vvalues, Ivalues = [], [], []
        channels = self.getChannelDict(powering)
        for channel in channels.keys():
            if self.getStatus(channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0) ":
                Svalues += ["ON"]
            elif self.getStatus(channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00 ":
                Svalues += ["OFF"]
            elif self.getStatus(channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1) ":
                Svalues += ["ILOCK"]
            else:
                Svalues += [self.getStatus(channel)]
            Vvalues += [self.getMeasurementSenseVoltage(channel)]
            Ivalues += [self.getMeasurementCurrent(channel)]
        return Svalues,Vvalues,Ivalues

    def write_log(self):
        powering_list = self.getPoweringList()
        f = open("Historical.log", "a")
        f.write(str(datetime.now()) + "\n")
        for powering in powering_list:
            channels = list(self.getChannelDict(powering).keys())
            log_data = self.measure(powering)
            #print(powering,channels,log_data)
            for i in range(len(log_data[0])):
                #print(str(channels[i]) +"\t"+ str(log_data[0][i]) + "\t" + str(log_data[1][i]) + " V \t" + str(log_data[2][i]) + " A\n")
                f.write(str(channels[i]) +"\t"+ str(log_data[0][i]) + "\t" + str(log_data[1][i]) + " V \t" + str(log_data[2][i]) + " A\n")
        f.close()
    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, powering, data):
        '''
        Inputs:         - Powering (i.e. light)
                        - Data (measurement array)

        Description:    Record timestamp on InfluxDB
        '''
        client = self.InitializeInfluxDB()
        channels = self.getChannelDict(powering)
        measurements_list = self.getMeasurementsList(powering)
        data = np.array(data)
        keys = list(channels.keys())
        for i in range(0,data.shape[1]) :
            data_column = data[:,i]
            client.write_points(self.JSON_setup(
                measurement = powering,
                channel_name = channels[keys[i]]["name"],
                status = data_column[0],
                fields = zip(measurements_list, 
                             [float(element) for element in data_column[1:]])
            ))
        client.close()

    def JSON_setup(self, measurement, channel_name, status, fields):
            '''
            Inputs:         - Measurement (i.e. light)
                            - Channel name (i.e. VGA_12_POS)
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
                    "channel_name" : channel_name,
                    "status" : status
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
        Inputs:         - Powering (i.e. light)

        Description:    Continuously record timestamp on InfluxDB
        '''
        try:
            print("Continuous DAQ Activated: " + powering + ". Taking data in real time")
            while self.getCrateStatus():
                data = self.measure(powering)
                self.INFLUX_write(powering,data)
                #self.write_log()
                time.sleep(2)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)