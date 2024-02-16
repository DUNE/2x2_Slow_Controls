from pysnmp.hlapi import *
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
from configparser import ConfigParser
import os

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
        
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def InitializeInfluxDB(self):
        '''
        Create InfluxDB client
        '''
        conf = ConfigParser()
        conf.read("app/CONFIG/config.ini")
        db = conf["DATABASE"]
        IP = os.environ.get("IP_LOCAL")
        # Run hostname -I to get local ip addresses
        client = InfluxDBClient(IP, db.get('PORT'), self.unit)
        if self.module == None:
            db_name = self.unit
        else:
            db_name = self.module + "_" + self.unit
        client.create_database(db_name)
        client.switch_database(db_name)
        return client 
    


    

