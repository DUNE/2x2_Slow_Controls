'''
--- Bruno Gelli
--- 12/05/2024

This code is intended to run on daq05. It has to be run together with the 
WhiteRabbit MIB (called WR-MIB.txt here).

This is was a really quick implementation. The code needs lots of work, but 
it will get the job done for now. 

points for the future:
	- write functions to organize the code
	- implement try:except instances to help debug in the future 
	- comments
'''

from influxdb import InfluxDBClient
from datetime import datetime
from subprocess import check_output
import time

client = InfluxDBClient('192.168.197.46',8086, 'lrs_monitor')
client.switch_database('lrs_monitor')

while True:

	now = datetime.utcnow().strftime('%Y%m%d %H:%M:%S')

	snmpOut = check_output("snmpget -c public -v 2c 192.168.197.81 -m /home/acd/acdcs/2x2/SlowControls2x2/WR/WR-MIB.txt wrsSystemClockDrift.0",shell=True,text=True)

	data = snmpOut.split('\n')

	driftVal = data[0].split(" ")[-1]

	json_body = [
	{
		"measurement": "WRSwitch",
		"tag": "TimeDrift",
		"time": now,
		"fields": {
			"drift": int(driftVal)
		}
	}
	]
	client.write_points(json_body)

	client.close()
	
	time.sleep(60)
