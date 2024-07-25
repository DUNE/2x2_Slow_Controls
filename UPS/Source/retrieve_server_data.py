import asyncio
from asyncua import Client

async def main():
    '''
    Function used to
    retrieve data from an OPC
    sever using asyncua
    '''

    url="opc.tcp://0.0.0.0:4840/freeopcua/server/"
    # Create a client instance
    async with Client(url) as client:
        print("Connected to the server")
        
        # Get the root node
        root = client.nodes.root
        print("Root node is: ", root)
        
        # Browse the root node
        objects = await root.get_child(["0:Objects"])
        print("Objects node is: ", objects)
        
        # Browse for a specific object/node
        myobj = await objects.get_child(["2:MyObject"])
        print("MyObject node is: ", myobj)
        
        # Get a variable node
        myvar = await myobj.get_child(["2:MyVariable"])
        print("MyVariable node is: ", myvar)
        
        # Read the value of the variable
        value = await myvar.read_value()
        print("Current value of MyVariable is: ", value)
        
        # Write a new value to the variable
        await myvar.write_value(100)
        print("Wrote new value to MyVariable")
        
        # Read the value again to confirm the change
        new_value = await myvar.read_value()
        print("New value of MyVariable is: ", new_value)
    

# Run the client script
if __name__ == "__main__":
    asyncio.run(main())

