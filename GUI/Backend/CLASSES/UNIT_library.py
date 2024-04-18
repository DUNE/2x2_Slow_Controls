from pysnmp.hlapi import *
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import os
import subprocess

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
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()  # Return the output of the command
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            self.execute_command(command)
            #return None
        
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def InitializeInfluxDB(self):
        '''
        Create InfluxDB client
        '''
        # Setup InfluxDB client
        IP = os.environ.get("IP_LOCAL")
        INFLUX_PORT = os.environ.get("INFLUX_PORT")
        client = InfluxDBClient(IP, INFLUX_PORT, self.unit)

        # Create database
        if self.module == None:
            db_name = self.unit
        else:
            db_name = self.module + "_" + self.unit
        client.create_database(db_name)

        # Switch to created database
        client.switch_database(db_name)
        return client 
    


    

