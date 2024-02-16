import socket, datetime, time
default_psu_ip ='192.168.196.33' #change ip
sample_interval_secs = 2.5
class ttiPsu(object):
    def __init__(self, ip, channel=1):
        self.ip = ip
        self.port = 9221 #default port for socket control
        #channel=1 for single PSU and right hand of Dual PSU
        self.channel = channel
        self.ident_string = ''
        self.sock_timeout_secs = 60
        self.packet_end = bytes('\r\n','ascii')
        #print('Using port', self.port)
        #print('using IP', self.ip)

    ##############################
    ### COMMUNICATION COMMANDS ###
    ##############################

    def send(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd,'ascii'))


    def recv_end(self, the_socket):
        total_data=[]
        data=''
        while True:
            data=the_socket.recv(1024)
            if self.packet_end in data:
                total_data.append(data[:data.find(self.packet_end)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if self.packet_end in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(self.packet_end)]
                    total_data.pop()
                    break
        return b''.join(total_data)

    # Sends and recieves a string
    def send_receive_string(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd,'ascii'))
            s.sendall(bytes(cmd,'ascii'))
            data = self.recv_end(s)
        return data.decode('ascii')

    # Sends and recieves a float
    def send_receive_float(self, cmd):
        r = self.send_receive_string(cmd)
        #Eg. '-0.007V\r\n'  '31.500\r\n'  'V2 3.140\r\n'
        r=r.rstrip('\r\nVA') #Strip these trailing chars
        l=r.rsplit() #Split to array of strings
        if len(l) > 0:
            return float(l[-1]) #Convert number in last string to float
        return 0.0

    # Sends and recieves an integer
    def send_receive_integer(self, cmd):
        r = self.send_receive_string(cmd)
        return int(r)

    # Sends and recieves a boolean
    def send_receive_boolean(self, cmd):
        if self.send_receive_integer(cmd) > 0:
            return True
        return False

    # Returns Ident
    def getIdent(self):
        self.ident_string = self.send_receive_string('*IDN?')
        return self.ident_string.strip()

    # Returns the configuration
    def getConfig(self):
        cmd = 'CONFIG?'
        v = self.send_receive_integer(cmd)
        return v

    ########################
    ### CURRENT COMMANDS ###
    ########################

    def getAmpRange(self):
        #Supported on PL series
        #Not supported on MX series
        r=0
        try:
            cmd = 'IRANGE{}?'.format(self.channel)
            r = self.send_receive_integer(cmd)
        except:
            pass
        #The response is 1 for Low (500/800mA) range,
        # 2 for High range (3A or 6A parallel)
        # or 0 for no response / not supported
        return r

    def setAmpRangeLow(self):
        #Supported on PL series
        #Not supported on MX series
        #Output must be switched off before changing range
        cmd = 'IRANGE{} 1'.format(self.channel)
        self.send(cmd)

    def setAmpRangeHigh(self):
        #Supported on PL series
        #Not supported on MX series
        #Output must be switched off before changing range
        cmd = 'IRANGE{} 2'.format(self.channel)
        self.send(cmd)

    # Set over current protection trip point
    def setTripAmps(self, amps):
        cmd = 'OCP{0} {1:1.3f}'.format(self.channel, amps)
        self.send(cmd)

    # Read current trip setting
    def getTripAmps(self):
        cmd = 'OCP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    # Set current limit of output
    def setMaxAmps(self, amps):
        cmd = 'I{0} {1:1.3f}'.format(self.channel, amps)
        self.send(cmd)

    # Returns current limit of output
    def getMaxAmps(self):
        #Reads output current
        #Output must be switched on to read.
        cmd = 'I{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v
    
    # Reads output current
    def readOutputAmps(self):
        cmd = 'I{}O?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    # Sets the voltage step size
    def setStepSizeAmps(self, step):
        cmd = 'DELTAI{0} {1:1.3f}'.format(self.channel, step)
        self.send(cmd)

    # Reads the step size (voltage)
    def readStepSizeAmps(self):
        cmd = 'DELTAI{}?'.format(self.channel)
        return self.send_receive_float(cmd)

    # Increments voltage
    def incrementCurrent(self):
        cmd = 'INCI{}'.format(self.channel)
        self.send(cmd)

    # Decremetns the voltage
    def decrementCurrent(self):
        cmd = 'DECI{}'.format(self.channel)
        self.send(cmd)

    #########################
    ### VOLTAGE COMMANDS  ###
    #########################

    # Set over voltage protection trip point
    def setTripVolts(self, volts):
        cmd = 'OVP{} {}'.format(self.channel, volts)
        self.send(cmd)

    # Read voltage trip setting
    def getTripVolts(self):
        cmd = 'OVP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v
    
    # Set output voltage
    def setMaxVolts(self, volts):
        cmd = 'V{0} {1:1.3f}'.format(self.channel, volts)
        self.send(cmd)
    
    # Return set output voltage
    def getMaxVolts(self):
        # Reads output voltage
        # Output must be switched on to read.
        cmd = 'V{0}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    # Reads output voltage
    def readOutputVolts(self):
        cmd = 'V{}O?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    # Sets the voltage step size
    def setStepSizeVolts(self, step):
        cmd = 'DELTAV{0} {1:1.3f}'.format(self.channel, step)
        self.send(cmd)

    # Reads the step size (voltage)
    def readStepSizeVolts(self):
        cmd = 'DELTAV{}?'.format(self.channel)
        return self.send_receive_float(cmd)

    # Increments voltage
    def incrementVoltage(self):
        cmd = 'INCV{}'.format(self.channel)
        self.send(cmd)

    # Decremetns the voltage
    def decrementVoltage(self):
        cmd = 'DECV{}'.format(self.channel)
        self.send(cmd)

    ########################
    ### VARIOUS COMMANDS ###
    ########################

    # Tell me if the output is enabled
    def getOutputIsEnabled(self):
        cmd = 'OP{}?'.format(self.channel)
        v = self.send_receive_boolean(cmd)
        return v

    # Sets Output to be either on/off
    def setOutputEnable(self, ON):
        cmd=''
        if ON == True:
            cmd = 'OP{} 1'.format(self.channel)
        else:
            cmd = 'OP{} 0'.format(self.channel)
        self.send(cmd)

    # Sets Local control
    def setLocal(self):
        cmd = 'LOCAL'
        self.send(cmd)

    # Gets data
    def GetData(self):
        # Gather data from PSU
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.mysocket = s
            self.mysocket.settimeout(self.sock_timeout_secs)
            self.mysocket.connect((self.ip, self.port))
            dtime = datetime.datetime.now()
            identity = self.getIdent()
            out_volts = self.getOutputVolts()
            out_amps = self.getOutputAmps()
            target_volts = self.getTargetVolts()
            target_amps = self.getTargetAmps()
            is_enabled = self.getOutputIsEnabled()
            amp_range = self.getAmpRange()
            #dataset = DataToGui(True, dtime, identity,
            #                        out_volts, out_amps,
            #                        target_volts, target_amps,
            #                        is_enabled, amp_range)
            return 1
    # Chooses static IP
    def chooseStaticIP(self):
        cmd = 'NETCONFIG STATIC'
        self.send(cmd)
    # Sets Static IP
    def setStaticIP(self):
        cmd = 'IPADDR 192.168.1.42'
        self.send(cmd)
