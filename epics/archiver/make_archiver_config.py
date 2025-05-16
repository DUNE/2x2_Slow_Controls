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
filename = 'ND2x2_archiver_config_20250516.xml'    
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
### == conclude the xml file
#################################
f = open(filename,'a')
f.write('</engineconfig>')
f.close()
