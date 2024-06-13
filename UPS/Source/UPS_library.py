from UNIT_library import UNIT
import socket
from datetime import datetime
import time 
import traceback
import sys


class UPS(UNIT):
    '''
    This class represents the template for a UPS system.
    '''
    def __init__(self):
        self.mib_dir = "../mibs_ups/"   # Need to declare a top directory for this 
        self.device_address = "192.168.197.92"
        self.battery_failure = self.get_battery_fail()
        self.battery_time = self.get_battery_time()
        self.battery_cap = self.get_battery_cap()

    def get_battery_fail(self):
        ups_stat_var = "xupsBatteryFailure.0"
        command = f"snmpget -v 3 -M +{self.mib_dir} -m ALL -u readonly -c public {self.device_address} {ups_stat_var}" 
        output_command = self.execute_command(command)
        temp_val = self.parse_snmpget_output(output_command)
        return temp_val['Value']
    
    def get_battery_time(self):
        ups_stat_var = "xupsBatTimeRemaining.0"
        command = f"snmpget -v 3 -M +{self.mib_dir} -m ALL -u readonly -c public {self.device_address} {ups_stat_var}" 
        output_command = self.execute_command(command)
        temp_val = self.parse_snmpget_output(output_command)
        return temp_val['Value']
    
    def get_battery_cap(self):
        ups_stat_var = "xupsBatCapacity.0"
        command = f"snmpget -v 3 -M +{self.mib_dir} -m ALL -u readonly -c public {self.device_address} {ups_stat_var}" 
        output_command = self.execute_command(command)
        temp_val = self.parse_snmpget_output(output_command)
        return temp_val['Value']



ups_a = UPS()
print(ups_a.device_address)
print(ups_a.battery_failure)
print(ups_a.battery_time)
print(ups_a.battery_cap)



