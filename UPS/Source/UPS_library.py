from UNIT_library import UNIT
import socket
from datetime import datetime
import time 
import traceback
import sys


class UPS(UNIT):
    '''
    This class represents the template to
    monitor an UPS system.
    '''
    def __init__(self):
        self.mib_dir = "../mibs_ups/"   # Need to declare a top directory for this 
        self.device_address = "192.168.197.92"
        self.battery_failure = self.get_battery_fail()
        self.battery_time = self.get_battery_time()
        self.battery_cap = self.get_battery_cap()
        self.battery_v = self.get_battery_voltage()
        self.battery_aged = self.get_battery_age()

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
    
    def get_battery_voltage(self):
        ups_stat_var = "xupsBatVoltage.0"
        command = f"snmpget -v 3 -M +{self.mib_dir} -m ALL -u readonly -c public {self.device_address} {ups_stat_var}" 
        output_command = self.execute_command(command)
        temp_val = self.parse_snmpget_output(output_command)
        return temp_val['Value']
    
    def get_battery_age(self):
        ups_stat_var = "xupsBatteryAged.0"
        command = f"snmpget -v 3 -M +{self.mib_dir} -m ALL -u readonly -c public {self.device_address} {ups_stat_var}" 
        output_command = self.execute_command(command)
        temp_val = self.parse_snmpget_output(output_command)
        return temp_val['Value']
    

    def CONTINUOUS_monitoring(self):
        '''
        Description:    Continuously record timestamp on InfluxDB
        '''
        print("Monitoring UPS system...")
        while True:
            print('Actual time: ', datetime.now())
            print('Battery failing? :', self.battery_failure['symbolic_name'])
            print('Battery capacity: ', self.battery_cap['value'])
            print('Battery voltage: ', self.battery_v['value'])
            print('Remaining battery time: ', self.battery_time['value'])
            time.sleep(10)



ups_a = UPS()
ups_a.CONTINUOUS_monitoring()




