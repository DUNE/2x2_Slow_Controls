import os

def start_group(filename, groupname, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''<group><name>{groupname}</name>
'''.format(groupname=groupname)
    f.write(this_line)
    f.close()
    
def end_group(filename, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''</group>
'''
    f.write(this_line)
    f.close()
    
def add_pv(filename, pvname, period, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''<channel><name>{pvname}</name><period>{period}</period><monitor/></channel>
'''.format(pvname=pvname, period=period)
    f.write(this_line)
    f.close()    


#### == Write an .xml file
filename = 'ND2x2_archiver_config_20250701.xml'    
f = open(filename,'w')
f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
f.write(
'''
<engineconfig>
'''
    )
f.close()

#################################
### == add testioc
#################################
start_group(filename, "testioc", 1)
add_pv(filename, "nd2x2_testioc/archive_test", "0.2", 2)
end_group(filename, 1)

#################################
### == add spellman HV
################################# 
start_group(filename, "SpellmanHV", 1)
add_pv(filename, "spellmanhv/rI", "0.2", 2)
add_pv(filename, "spellmanhv/rV", "0.2", 2)
end_group(filename, 1)

#################################
### == add MPODs
#################################
channel_pvs = ["outputMeasurementCurrent", "outputMeasurementSenseVoltage", "outputMeasurementTerminalVoltage", "outputStatus"]
crate_pvs = ["sysStatus", "sysMainSwitch"]
start_group(filename, "MPOD", 1)
for module in range(0, 4):
    this_module = "Mod" + str(module)
    ## -- Add VGA
    for vga in range(1, 5):
        this_vga = this_module + "-VGA_Card_" + str(vga)
        for channel_pv in channel_pvs:
            this_pv = this_vga + "/" + channel_pv
            add_pv(filename, this_pv, "0.2", 2)

    ## -- Add RTD
    if module == 0:
        for rtds in range(1, 3):
            this_rtd = this_module + "-RTD_" + str(rtds)
            for channel_pv in channel_pvs:
                this_pv = this_rtd  + "/" + channel_pv
                add_pv(filename, this_pv, "0.2", 2)
    else:
        this_rtd = this_module + "-RTD"
        for channel_pv in channel_pvs:
            this_pv = this_rtd  + "/" + channel_pv
            add_pv(filename, this_pv, "0.2", 2)

    ## -- Add PACFAN & PACMAN
    for tpc in range(1, 3):
        this_tpc = this_module + "-TPC" + str(tpc)

        ## -- PACFAN & PACMAN
        for channel_pv in channel_pvs:
            this_pv = this_tpc  + "_pacFAN/" + channel_pv
            add_pv(filename, this_pv, "0.2", 2)
            this_pv = this_tpc  + "_PACMAN/" + channel_pv
            add_pv(filename, this_pv, "0.2", 2)

    ## interlock
    if module != 2:
        this_interlock = this_module + "-interlock"
        for channel_pv in channel_pvs:
            this_pv = this_interlock  + "_pacFAN/" + channel_pv
            add_pv(filename, this_pv, "0.2", 2)

for mpod in range(0, 2):
    this_mpod = "mpod" + str(mpod)
    for crate_pv in crate_pvs:
        this_pv = this_mpod + "/" + crate_pv
        add_pv(filename, this_pv, "0.2", 2)
end_group(filename, 1)

#################################
### == conclude the xml file
#################################
f = open(filename,'a')
f.write('</engineconfig>')
f.close()
