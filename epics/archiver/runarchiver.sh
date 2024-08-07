#!/bin/bash
# NB: Make sure archiver_helper is using the correct "engine"
#

source ~/2x2/EPICS/setup_EPICS.sh
cd /home/acd/acdcs/2x2/EPICS/phoebus/phoebus/services/archive-engine

./archive-engine.sh -engine ND2x2 -port 4812 -settings /home/acd/acdcs/2x2/EPICS/2x2_Slow_Controls/epics/archiver/archiver.ini
