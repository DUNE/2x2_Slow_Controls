TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = SpellmanHV
# SpellmanHV.dbd will be created and installed
DBD += SpellmanHV.dbd

# SpellmanHV.dbd will be made up from these files:
SpellmanHV_DBD += base.dbd

# Include dbd files from all support applications:
#SpellmanHV_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#SpellmanHV_LIBS += xxx

# SpellmanHV_registerRecordDeviceDriver.cpp derives from SpellmanHV.dbd
SpellmanHV_SRCS += SpellmanHV_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
SpellmanHV_SRCS_DEFAULT += SpellmanHVMain.cpp
SpellmanHV_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#SpellmanHV_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
SpellmanHV_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

#DBD
SpellmanHV_DBD += calcSupport.dbd
SpellmanHV_DBD += stream.dbd
SpellmanHV_DBD += drvAsynSerialPort.dbd
SpellmanHV_DBD += drvAsynIPPort.dbd
#SpellmanHV_DBD += calcSupport.dbd
SpellmanHV_DBD += asyn.dbd

#LIB
SpellmanHV_LIBS += stream
SpellmanHV_LIBS += asyn
SpellmanHV_LIBS += calc
