#!/usr/bin/python
import time, math, json
import datetime 
import subprocess
import asyncio 
from asyncua import Server, ua 
import socket 

async def main():
    '''
    This is just an example for now...
    It creates a server with a variable
    that stores the date and time after every second
    '''


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
    myobj = await objects.add_object(idx, "MyObject")
    
    # Add a variable to the new object
    myvar = await myobj.add_variable(idx, "MyVariable", 0, ua.String)
    
    # Make the variable writable by clients
    await myvar.set_writable()
    
    # Start the server
    await server.start()
    print("OPC UA Server is running...")
    
    try:
        # Update the variable in a loop
        while True:
            time_now = datetime.datetime.now()
            # Format the date as a string
            date_string = time_now.strftime("%Y-%m-%d-%H-%M-%S")
            await myvar.write_value(date_string)
            print(f"Set variable value to {date_string}")
            await asyncio.sleep(1)  # Sleep for 1 second
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server
        await server.stop()
        print("OPC UA Server has stopped.")


if __name__ == "__main__":
    asyncio.run(main())

