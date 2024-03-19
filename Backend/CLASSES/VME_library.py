from app.CLASSES.UNIT_library import UNIT
from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import traceback
import sys

class VME(UNIT):
    '''
    This class represents the template for a VME.
    '''
    def __init__(self, module, unit, dict_unit, miblib='CONFIG/mibs_vme'):
        '''
        Unit constructor
        '''
        self.miblib = miblib
        super().__init__(module, unit)
        self.dictionary = dict_unit
        self.crate_status = self.getCrateStatus()
        self.measuring_status = self.getMeasuringStatus()

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def vmeSwitch(self, vmen, switch):
        os.popen("snmpset -v 2c -M " + str(self.miblib) + " -m +WIENER-CRATE-MIB -c guru " + str(self.ip[vmen]) + " sysMainSwitch.0 i " + str(switch))
        #os.popen("snmpset -v 2c -M ./mibs -m +WIENER-CRATE-MIB -c guru " + self.ip[0] + " sysMainSwitch.0 i " + str(switch))

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def getTemperature(self, vmen, sensor):
        '''
        Returns the Temperature of the sensor
        '''
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " sensorTemperature" + sensor)
        ret = data.read().split('\n')
		
        return ret[0].split(" ")[-2]
    
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