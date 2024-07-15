# White rabbit time drift 
This is a code to querie the White Rabbit for the time difference between its internal clock and NTP. 

## How it works
It works based on a SNMP request. 
The code requests the time difference using the following command.
```
snmpget -c public -v 2c 192.168.197.81 -m /home/acd/acdcs/2x2/SlowControls2x2/WR/WR-MIB.txt wrsSystemClockDrift.0
```
This will return a string with some information and a integer number of seconds of drift. Some string manipulation is done to get the reply into the right format.

After getting the right format, a json payload is assembled and pushed to the InfluxDB instance on daq05. (lrs_monitor bucket)

The is repeted once a minute. Since the time drifft is expected to not change from 0, this is done to reduce the storage and network impact of the code.

## How to run the code
This code is intended to run on daq05. It has to be run on the same folder as the WhiteRabbit MIB (Called WR-MIB.txt), so snmpget gets the right path. If you move the code somewhere else (container maybe?), make sure to ajust the snmpget path. 

To run it, simply call `python3 wrtimedrift.py3 &`. This will start the code in the background. Check on grafana if data is being pushed correctly

## Improvements
- Organize the code with functions
- Improve/implement error handlying
- Improve commenting 
