import socket
import sys
import os
import subprocess
import time
from influxdb import InfluxDBClient
from datetime import datetime
import pytz
from configparser import ConfigParser

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Arg1:', str(sys.argv[1])
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Get SpellmanIP
conf = ConfigParser()
try:
     conf.read("config.ini")
except FileNotFoundError:
     conf.read("./SPELLMAN/config.ini")

Spellman = conf['SpellMan']
# Connect the socket to the port where the server is listening
server_address = (Spellman['IP'], 50001)
#print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    if len(sys.argv) == 1:
        print("Usage: ")
        print("python SpellmanCTL.py [CMD]")
        print(" Clear - clear fault flags, disable HV")
        print(" IsON  - returns 1 if HV is ON, 0 otherwise")
        print(" Enable  - enables HV (remote mode only)")
        print(" Disable - disables HV (remote mode only)")
        print(" GetSP_V - print set voltage")
        print(" GetSP_I - print set current limit")
        print(" GetVI - print actual voltage [kV] and current [mA]")
        print(" SetSP_V [kV] - set setpoint for voltage (remote mode only)")
        print(" SetSP_I [mA] - set current limit (remote mode only)")
        print(" OpMode - print operation mode (voltage/current limit)")
        print(" Status - prints status flags")
        print("RampTo [kV] - Ramps HV up to voltage given [kV]")
    
    elif str(sys.argv[1]) == 'IsON':
        message = b"\x02"+b'22,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[9:10] 
             print(str(val))
        else: print('Error')  
    
    elif str(sys.argv[1]) == 'Clear':     
        message = b"\x02"+b'52,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  

    elif str(sys.argv[1]) == 'Enable':     
        message = b"\x02"+b'99,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  

    elif str(sys.argv[1]) == 'Disable':     
        message = b"\x02"+b'98,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  
    
    elif str(sys.argv[1]) == 'GetSP_V':     
        message = b"\x02"+b'14,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
#        if len(data)>=0 and len(data)<=100: 
             val=data.split(",")[1] 
             fval=50.0 / 4095 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'GetSP_I':     
        message = b"\x02"+b'15,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             fval=6.0 / 4095 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'GetVI':     
        message = b"\x02"+b'20,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=7: 
             val=data.split(",")[9] 
             fval=50.0 / 3983 * float(str(val))
             print(str(fval))
             val=data.split(",")[2] 
             fval=6.0 / 3983 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'SetSP_V': 
        if len(sys.argv) == 2: 
             val=0
        else:
             val= int(float(sys.argv[2])/50.0*4095)
        print('Sending '+str(val))
        message = b"\x02"+b'10,' + bytes(str(val), 'utf-8') + b','+b"\x03"
#        print str(message)
        sock.sendall(message)
        data = str(sock.recv(32))
#        print str(data)
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error. Works only in remote mode')  

    elif str(sys.argv[1]) == 'SetSP_I': 
        if len(sys.argv) == 2: 
             val=0
        else:
             val= int(float(sys.argv[2])/6.0*4095)
        message = b"\x02"+b'11,' + bytes(str(val),'utf-8') + b','+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error. Works only in remote mode')  

    elif str(sys.argv[1]) == 'OpMode':     
        message = b"\x02"+b'69,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=16: 
             val=data.split(",")[1] 
             print("Current mode " + str(val))
             val=data.split(",")[2] 
             print("Voltage mode " + str(val))
        else: print('Error')  


    elif str(sys.argv[1]) == 'Status':     
        message = b"\x02"+b'32,'+b"\x03"
        sock.sendall(message)
        data = sock.recv(32)
        if len(data)==27: 
             print(data)
             val=data[4:25]
             print(val) 
             print("Interlock OK "+str(val).split(",")[0]) 
             print("HV Inhibit (?) "+str(val).split(",")[1]) 
             print("Overvoltage  "+str(val).split(",")[2]) 
             print("Overcurrent  "+str(val).split(",")[3]) 
             print("Overpower    "+str(val).split(",")[4]) 
             print("Regulator error "+str(val).split(",")[5]) 
             print("Arcing detected "+str(val).split(",")[6]) 
             print("Overtemperature "+str(val).split(",")[7]) 
             print("Adj overload fault "+str(val).split(",")[8]) 
             print("System fault "+str(val).split(",")[9]) 
             print("Remote mode  "+str(val).split(",")[10]) 
        else: print('Error')  

    elif str(sys.argv[1]) == 'RampTo':
        if len(sys.argv) == 2:
             target_val=0
        else:
             target_val= float(sys.argv[2])

        #get current set point
        message = b"\x02"+b'14,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             cur_sp=50.0 / 4095 * float(str(val))
             print('Current value'+ str(cur_sp))
        else: print('Error')  
        step=0.01
        if cur_sp<target_val :
             print('Ramping UP to '+str(target_val))
             inc=step 
        elif cur_sp>target_val :
             print('Ramping DOWN to '+str(target_val))
             inc=-step
        else:
             print('Already at '+str(target_val))
             inc=0;
        sp=cur_sp
        while abs(sp-target_val) > step:
             sp=sp+inc
             val=int(sp/50.0*4095)
             print('Ramping: '+ str(sp), end='\r')
             message = b"\x02"+b'10,' + bytes(str(val), 'utf-8') + b','+b"\x03"
             sock.sendall(message)
             data = str(sock.recv(32))
             if len(data)==16:
                val=data[9:10]
                #print( str(val))
             else: print('Error. Works only in remote mode')
             time.sleep(0.1)
        if abs(sp-target_val) <= step:
             val = int(target_val/50.0*4095)
             message = b"\x02"+b'10,' + bytes(str(val), 'utf-8') + b','+b"\x03"
             sock.sendall(message)
             data = str(sock.recv(32))
             if len(data)==16:
                val=data[9:10]
                print(str(val))
             else: print('Error. Works only in remote mode')
             time.sleep(0.5)

        print('Voltage value is set to: ' + str(target_val))

    elif str(sys.argv[1]) == 'SendToDB':

        client = InfluxDBClient('192.168.197.46', 8086, 'HVmonitoring')
        #client.create_database('HVmonitoring')
        client.switch_database('HVmonitoring')
        #client.get_list_database()
        json_payload = []


        message = b"\x02"+b'20,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=7: 
             VMON=data.split(",")[9] 
             f_VMON=50.0 / 3983 * float(str(VMON))
             #print('Vmon: '+str(fval))
             FNULL = open(os.devnull, 'w')  
             IMON=data.split(",")[2] 
             f_IMON=6.0 / 3983 * float(str(IMON))
             #print('Imon: '+str(fval))
                  
        else: print('Error')  
                
#            elif str(sys.argv[1]) == 'GetSP_V':     
        message = b"\x02"+b'14,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
#        if len(data)>=0 and len(data)<=100: 
             voltage=data.split(",")[1] 
             f_voltage=50.0 / 4095 * float(str(voltage))
             #print('SP_V: '+str(f_voltage))       
        else: print('Error')  

 #   elif str(sys.argv[1]) == 'GetSP_I':     
        message = b"\x02"+b'15,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
             current=data.split(",")[1] 
             f_current=6.0 / 4095 * float(str(current))
             #print('SP_I: '+str(f_current))
               
        else: print('Error')  


        message = b"\x02"+b'22,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             Enabled=int(data[9:10])  
             #print('Enabled: '+str(Enabled))       
        else: print('Error')  
        
        utc_timezone = datetime.utcnow().strftime('%Y%m%d %H:%M:%S')
        #fermi_timezone = pytz.timezone('America/Chicago')
        #fermi_time = utc_timezone.astimezone(fermi_timezone)
        #fermi_time_str = fermi_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        
        data = {#Table name
                "measurement": "SPELLMAN_HV",
                
                #Time Stamp
                "time" : utc_timezone,
                
                #Data Fields
                "fields" : {"Voltage": f_voltage,
                            "Current": f_current,
                            "VMON": f_VMON,
                            "IMON": f_IMON,
                            "Enabled": Enabled
                            }
                }
        json_payload.append(data)
        client.write_points(json_payload)
        
    else: print('Unrecognized command')   
finally:
#    print >>sys.stderr, 'closing socket'
    sock.close()
