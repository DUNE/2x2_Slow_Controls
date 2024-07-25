#!/usr/bin/python
import time, math, json
import datetime 
import subprocess
import asyncio 
from asyncua import Server, ua 
from UPS_library import UPS
import socket 



async def main():
    '''
    This is just an example for now...
    It creates a server with a variable
    that stores the date and time after every second
    '''

    # UPS to monitor
    ups = UPS("192.168.197.92")

    # Create server instance
    server = Server() 
    # Set server endpoint
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    
    # Setup server namespaces
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # Get the Objects node, which is the root node for our server
    objects = server.nodes.objects
    
    # Add a new object to the server
    myobj = await objects.add_object(idx, "UPSSet")
    
    # Add a variables to store UPS data
    date_var = await myobj.add_variable(idx, "DateVar", 0, ua.String)
    # Testing with string for now...
    battery_time = await myobj.add_variable(idx,"BatTime",0,ua.String)

    # Make the variable writable by clients
    await date_var.set_writable()
    await battery_time.set_writable()
    
    # Start the server
    await server.start()
    print("OPC UA Server is running...")
    
    try:
        # Update the variable in a loop
        while True:
            time_now = datetime.datetime.now()
            # Format the date as a string
            date_string = time_now.strftime("%Y-%m-%d-%H-%M-%S")
            await date_var.write_value(date_string)
            #print(f"Set variable value to {date_string}")
            await battery_time.write_value(
                ups.get_battery_time()['value']
            )
            await asyncio.sleep(10)  # Sleep for 1 second
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server
        await server.stop()
        print("OPC UA Server has stopped.")


if __name__ == "__main__":
    asyncio.run(main())

