#from pysnmp.hlapi import *
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import os
import subprocess,time
from subprocess import check_output
import re


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
        

    def parse_snmpget_output(self,output):
        # Split the output string to separate OID, TYPE, and VALUE
        split_output = output.split('=', 1)
        if len(split_output) > 1:
            oid_part = split_output[0].strip()
            type_value_part = split_output[1].strip()
            
            type_value_split = type_value_part.split(':', 1)
            if len(type_value_split) > 1:
                value_type = type_value_split[0].strip()
                value = type_value_split[1].strip()
                
                # Extract symbolic name and numeric value if present
                match = re.match(r'(.+?)\((\d+)\)', value)
                if match:
                    symbolic_name = match.group(1).strip()
                    numeric_value = int(match.group(2).strip())
                    value = {'symbolic_name': symbolic_name, 'numeric_value': numeric_value}
                else:
                    value = {'value': value.strip()}
            
            else:
                value_type = None
                value = type_value_part.strip()
            return {'OID': oid_part, 'Type': value_type, 'Value': value}
        else:
            return None

        
    #def parse_mib_int(int):

    #def parse_mib_boolean(boolean):


        
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
    


    

