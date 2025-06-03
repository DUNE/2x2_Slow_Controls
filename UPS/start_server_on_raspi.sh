#!/usr/bin/bash                                                                                                                                                                                                    

##########################                                                                                                                                                                                         
#### This script starts the OPC-UA server for you                                                                                                                                                                  
#### The RasPi runs this scripts everytime the its rebooted                                                                                                                                                        
##########################                                                                                                                                                                                         


echo "Starting OPCUA server..."

# Go to UPS dir and setup dir                                                                                                                                                                                      

cd /home/acd-raspi-ups/Monitoring/2x2_Slow_Controls/UPS


source setup.sh

# Start the server                                                                                                                                                                                                 
# Store the nohup output into a log file                                                                                                                                                                           
current_datetime=$(date +"%Y-%m-%d-%H:%M:%S")

# Create logs directory 
mkdir -p logs 

nohup python /home/acd-raspi-ups/Monitoring/2x2_Slow_Controls/UPS/Source/UPS_with_opcua.py > /home/acd-raspi-ups/Monitoring/2x2_Slow_Controls/UPS/logs/ups_server_${current_datetime}.log 2>&1 &
