TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build an IOC support library

#=============================
# Build the IOC application

PROD_IOC = testioc
# testioc.dbd will be created and installed
DBD += testioc.dbd

# testioc.dbd will be made up from these files:
testioc_DBD += base.dbd

# Include dbd files from all support applications:
#testioc_DBD += xxx.dbd

# Add all the support libraries needed by this IOC

# testioc_registerRecordDeviceDriver.cpp derives from testioc.dbd
testioc_SRCS += testioc_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
testioc_SRCS_DEFAULT += testiocMain.cpp
testioc_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
testioc_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
testioc_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

