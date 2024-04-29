#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 134 HAT Temp reader

    Purpose:
        Read temp values from raspi hat and push to influxdb

"""

from __future__ import print_function
import time
from sys import stdout
import sys, os
#sys.path.append('/home/pi/daqhats')
from daqhats import mcc134,mcc118, OptionFlags, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, enum_mask_to_string, tc_type_to_string
import subprocess

import configparser

from datetime import datetime
import pytz
from influxdb import InfluxDBClient

conf = configparser.ConfigParser()
conf.read('/home/pi/Dune2x2_SlowControl/config.ini')

db = conf["DATABASE"]
meta = conf["METADATA"]
para = conf["PARAMETERS"]

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'
OFFSET_SENS_A = 0.0
OFFSET_SENS_B = 0.0
OFFSET_SENS_C = 0.0
ped = [146.1,152.4,147.3,147.3]
kv = [0.01106,0.01098,0.01094,0.01092]

client = InfluxDBClient(host = db["IP"], port = int(db["PORT"]), database = db["NAME"])

def main():
    """
    This function is executed automatically when the module is run directly.
    """
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    channels_tc = {0}
    channels_adc = {0,1,2,3}

    try:
        # Get an instance of the selected hat device object.
        address_tc = select_hat_device(HatIDs.MCC_134)
        address_adc = select_hat_device(HatIDs.MCC_118)
        hat_tc = mcc134(address_tc)
        hat_adc = mcc118(address_adc)
        for channel in channels_tc:
            hat_tc.tc_type_write(channel, tc_type)
        
        print('    Thermocouple type: ' + tc_type_to_string(tc_type))
        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\n  Sample', end='')
        for channel in channels_tc:
            print('       TC ', channel, end='')
        for channel in channels_adc:
            print('          V',channel, end='')
        print('')
        
        try:
            samples_per_channel = 0
            json_payload = []
            
            while True:
                # Display the updated samples per channel count
                samples_per_channel += 1
                print('\r{:8d}'.format(samples_per_channel), end='')
                
                # Read TCs
                for channel in channels_tc:
                    temp_value = hat_tc.t_in_read(channel)
                    
                    #corr = (hat_tc.cjc_read(channel)-24.3)*1.7
                    #value=value - corr + 4.5
                    #value = hat_tc.a_in_read(channel)*1000
                    #if channel == 0:
                        #position = "A"
                        #value += OFFSET_SENS_A
                    
                    if temp_value == mcc134.OPEN_TC_VALUE:
                        print('     Open     ', end='')
                    elif temp_value == mcc134.OVERRANGE_TC_VALUE:
                        print('     OverRange', end='')
                    elif temp_value == mcc134.COMMON_MODE_TC_VALUE:
                        print('   Common Mode', end='')
                    else:
                        print('{:12.2f} '.format(temp_value), end='')
                        
                values_adc = []
                
                # Read ADC
                for channel in channels_adc:
                    value_adc = hat_adc.a_in_read(channel)
                    value_adc = value_adc*1000.-ped[channel]
                    value_adc *= kv[channel]
                    print('{:12.2f} '.format(value_adc), end='')
                    values_adc.append(value_adc)
                    
                #Get correct time for influx
                utc_timezone = datetime.utcnow()
                fermi_timezone = pytz.timezone('America/Chicago')
                fermi_time = utc_timezone.astimezone(fermi_timezone)
                fermi_time_str = fermi_time.strftime('%Y-%m-%d %H:%M:%S.%f') 
                
                #Write data to json payload and send to InfluxDB
                data = {#Table name
                        "measurement":"Raspi",
                        #Time Stamp
                        "time": fermi_time_str,
                        #Data Fields
                        "fields":{"Temperature":temp_value, "CH0":values_adc[0], "CH1":values_adc[1],"CH2":values_adc[2],"CH3":values_adc[3]}
                        }

                json_payload.append(data)
                client.write_points(json_payload)
                json_payload.clear()
                stdout.flush()

                # Wait the specified interval between reads.
                time.sleep(int(para["CTIME"]))

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
