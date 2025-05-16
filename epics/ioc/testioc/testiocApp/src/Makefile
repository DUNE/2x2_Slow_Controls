TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build an IOC support library

#=============================
# Build the IOC application

PROD_IOC = testiocApp
# testiocApp.dbd will be created and installed
DBD += testiocApp.dbd

# testiocApp.dbd will be made up from these files:
testiocApp_DBD += base.dbd

# Include dbd files from all support applications:
#testiocApp_DBD += xxx.dbd

# Add all the support libraries needed by this IOC

# testiocApp_registerRecordDeviceDriver.cpp derives from testiocApp.dbd
testiocApp_SRCS += testiocApp_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
testiocApp_SRCS_DEFAULT += testiocAppMain.cpp
testiocApp_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
testiocApp_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
testiocApp_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

