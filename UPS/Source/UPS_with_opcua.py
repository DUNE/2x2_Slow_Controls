#!/usr/bin/python
import time, math, json
import datetime 
import subprocess
import asyncio 
from asyncua import Server, ua 
from UPS_library import UPS
from utils import parse_config
import socket 
import os 
from pytz import timezone 

async def main():

    ''' This script starts a OPCUA server.
    The server queries the UPS using snmp
    and stores the values obtained into
    variables. The variables can be accessed 
    by other devices connected to the same
    network
    '''
    cfg = os.getenv('TOP_DIR') +"/config/UPS.cfg"
    input_par = parse_config(cfg)
    IP = input_par['ups_ip']
    PORT = input_par['port']
    # UPS to monitor
    ups = UPS(IP)

    # Create server instance
    server = Server() 
    # Set server endpoint
    await server.init()
    server.set_endpoint(f"opc.tcp://0.0.0.0:{PORT}/freeopcua/server/")
    
    # Setup server namespaces
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # Get the Objects node, which is the root node for our server
    objects = server.nodes.objects
    
    # Add a new object to the server
    myobj = await objects.add_object(idx, "UPSSet")
    
    # Add a variables to store UPS data
    date_var = await myobj.add_variable(idx, "DateVar", 0, ua.String)

    # Battery variables 
    battery_time = await myobj.add_variable(idx,"BatTime",0,ua.String)
    battery_fail = await myobj.add_variable(idx,"BatFail",0,ua.String)
    battery_cap = await myobj.add_variable(idx,"BatCap",0,ua.String)
    battery_v = await myobj.add_variable(idx,"BatV",0,ua.String)
    battery_age = await myobj.add_variable(idx,"BatAge",0,ua.String)

    # Input variables
    input_voltage = await myobj.add_variable(idx,"InV",0,ua.String)
    input_current = await myobj.add_variable(idx,"InC",0,ua.String)

    # Output variables
    output_voltage = await myobj.add_variable(idx,"OutV",0,ua.String) 
    output_current = await myobj.add_variable(idx,"OutC",0,ua.String)
    output_power = await myobj.add_variable(idx,"OutP",0,ua.String)

    # Make the variable writable by clients
    await date_var.set_writable()
    await battery_time.set_writable()
    await battery_fail.set_writable()
    await battery_cap.set_writable()
    await battery_v.set_writable()
    await battery_age.set_writable()
    await input_voltage.set_writable()
    await input_current.set_writable()
    await output_voltage.set_writable()
    await output_current.set_writable()
    await output_power.set_writable()

    # Start the server
    await server.start()
    print("OPC UA Server is running...")
    
    try:
        # Update the variable in a loop
        while True:
            # Format the date as a string
            chicago_time = timezone("America/Chicago")
            time_now = datetime.datetime.now(chicago_time)
            date_string = time_now.strftime("%Y-%m-%d-%H-%M-%S")
            await date_var.write_value(date_string)
            #print(f"Set variable value to {date_string}")

            # Write variables 
            await battery_time.write_value(
                ups.get_battery_time()['value']
            )

            await battery_fail.write_value(
                ups.get_battery_fail()['symbolic_name']
            )
            await battery_cap.write_value(
                ups.get_battery_cap()['value']
            )
            await battery_v.write_value(
                ups.get_battery_voltage()['value']
            )
            await battery_age.write_value(
                ups.get_battery_age()['symbolic_name']
            )

            await input_voltage.write_value(
                ups.get_input_voltage()['value']
            )
            
            await input_current.write_value(
                ups.get_input_current()['value']
            )

            await output_voltage.write_value(
                ups.get_output_voltage()['value']
            )

            await output_current.write_value(
                ups.get_output_current()['value']
            )

            await output_power.write_value(
                ups.get_output_power()['value']
            )

            await asyncio.sleep(5)  # Sleep for 10 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server
        await server.stop()
        print("OPC UA Server has stopped.")


if __name__ == "__main__":
    asyncio.run(main())

