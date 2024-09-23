#from pysnmp.hlapi import *
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import os
import subprocess,time
from subprocess import check_output


#from pydantic import BaseModel

class UNIT():
    '''
    This class represents the template for power supplies such as mpods, TTIs, etc.
    '''
    def __init__(self, module, unit):
        #Unit device constructor
        self.module = module
        self.unit = unit
        self.error_status = False

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # GET METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def getUnit(self):
        return self.unit
    
    def getModule(self):
        return self.module
    
    def execute_command(self, command):
        try:
            output = check_output(command, shell=True, text=True)
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            output = self.execute_command(command)
            return output
        
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def InitializeInfluxDB(self):
        '''
        Create InfluxDB client
        '''
        # Setup InfluxDB client
        IP = "192.168.197.46"
        INFLUX_PORT = "8086"
        db_name = self.module + "_" + self.unit + "_TEST"
        client = InfluxDBClient(IP, INFLUX_PORT, db_name)

        # Create database
        client.create_database(db_name)
        
        # Switch to created database
        client.switch_database(db_name)
        return client 
    


    

