import socket
import sys
import os
import subprocess
import time
import atexit

class Spellman: 
   def __init__(self, SpellmanIP):
       self.ip = SpellmanIP
       self.V = 0;
       self.I = 0;
       atexit.register(self.close)
       self.open() 

   def open(self):
       print('Opening socket.')
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       server_address = (self.ip, 50001)
       self.sock.connect(server_address)
       return 1

   def close(self):
       print('Closing socket.')
       self.sock.close()
       return 1
       
       
   def GetSP_V(self):
       message = b"\x02"+b'14,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             fval=50.0 / 4095 * float(str(val))
             print('GetSP_V: '+str(fval)+' kV')
             return fval
       else: 
             print('GetSP_V: Communication error')  
             return -1
             
   def GetSP_I(self):
       message = b"\x02"+b'15,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             fval=6.0 / 4095 * float(str(val))
             print('GetSP_I: '+str(fval)+' mA')
             return fval
       else: 
             print('GetSP_I: Communication error')  
             return -1


   def SetSP_V(self, sp):
        val= int(sp/50.0*4095)
        message = b"\x02"+b'10,' + bytes(str(val), 'utf-8') + b','+b"\x03"
        self.sock.sendall(message)
        data = str(self.sock.recv(32))
        if len(data)==16: 
             val=data[9:10] 
             print('SetSP_V reply: '+str(val))
             return 1
        else: 
             print('SetSP_V Error: Works only in remote mode')  
             return -1
             
   def SetSP_I(self,sp):
        val= int(sp/6.0*4095)
        message = b"\x02"+b'11,' + bytes(str(val),'utf-8') + b','+b"\x03"
        self.sock.sendall(message)
        data = str(self.sock.recv(32))
        if len(data)==16: 
             val=data[9:10] 
             print('SetSP_I reply: '+str(val))
             return 1
        else: 
             print('SetSP_I: Communication error')  
             return -1


   def Get_VI(self):
       message = b"\x02"+b'20,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(64))
       if len(data)>=7: 
             val=data.split(",")[9] 
             self.V=50.0 / 3983 * float(str(val))
             val=data.split(",")[2] 
             self.I=6.0 / 3983 * float(str(val))
             print('Get_VI: '+str(self.V)+' kV; '+str(self.I)+' mA')
             return 1
       else: 
             print('Get_VI: Communication error')  
             return -1



   def IsON(self):
       message = b"\x02"+b'22,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)==16: 
             val=data[9:10] 
             print(str(val))
             return val
       else: 
             print('IsON: Comm Error')  
             return -1
    
   def Clear(self):
       message = b"\x02"+b'52,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)==16: 
             val=data[9:10] 
             print(str(val))
             return 1
       else: 
             print('Clear: Comm Error')  
             return -1

   def Enable(self):
       message = b"\x02"+b'99,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)==16: 
             val=data[9:10] 
             print(str(val))
             return 1
       else: 
             print('Enable: Comm Error')  
             return -1

   def Disable(self):
       message = b"\x02"+b'98,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(32))
       if len(data)==16: 
             val=data[9:10] 
             print(str(val))
             return 1
       else: 
             print('Disable: Comm Error')  
             return -1

   def GetOpMode(self):
       message = b"\x02"+b'69,'+b"\x03"
       self.sock.sendall(message)
       data = str(self.sock.recv(64))
       if len(data)>=16: 
             val=data.split(",")[1] 
             print("GetOpMode: Current mode " + str(val))
             val=data.split(",")[2] 
             print("GetOpMode: Voltage mode " + str(val))
             return 1
       else: 
             print('GetOpMode: Comm Error')  
             return -1

             
   def PrintStatus(self):
       message = b"\x02"+b'32,'+b"\x03"
       self.sock.sendall(message)
       data = self.sock.recv(32)
       if len(data)==27: 
             val=data[4:25] 
             print("Spellman status bits: ") 
             print(" Interlock OK "+str(val).split(",")[0]) 
             print(" HV Inhibit (?) "+str(val).split(",")[1]) 
             print(" Overvoltage  "+str(val).split(",")[2]) 
             print(" Overcurrent  "+str(val).split(",")[3]) 
             print(" Overpower    "+str(val).split(",")[4]) 
             print(" Regulator error "+str(val).split(",")[5]) 
             print(" Arcing detected "+str(val).split(",")[6]) 
             print(" Overtemperature "+str(val).split(",")[7]) 
             print(" Adj overload fault "+str(val).split(",")[8]) 
             print(" System fault "+str(val).split(",")[9]) 
             print(" Remote mode  "+str(val).split(",")[10]) 
       else: print('PrintStatus: Comm Error')  

             
      
