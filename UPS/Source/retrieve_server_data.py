import asyncio
from asyncua import Client

async def retrieve_data():
    '''
    Function used to
    retrieve data from an OPC
    sever using asyncua
    '''
    url="opc.tcp://192.168.197.91:4840/freeopcua/server/"
    # Create a client instance
    async with Client(url) as client:
        print("Connected to the server")
        
        # Get the root node
        root = client.nodes.root
        #print("Root node is: ", root)
        
        # Browse the root node
        objects = await root.get_child(["0:Objects"])
        #print("Objects node is: ", objects)
        
        # Browse for a specific object/node
        myobj = await objects.get_child(["2:MyObject"])
        print("MyObject node is: ", myobj)
        
        # Get a variable node
        myvar_date = await myobj.get_child(["2:DateVar"])
        print("MyVariable node is: ", myvar_date)
        
        # Read the value of the variable
        date = await myvar_date.read_value()

        # Get a variable node
        myvar_bat_time = await myobj.get_child(["2:BatTime"])
        print("MyVariable node is: ", myvar_bat_time)
        
        # Read the value of the variable
        bat_time = await myvar_bat_time.read_value()


        print("Current date is: ", date)
        print("Remaining battery time: ", bat_time)
        
    

# Run the client script
if __name__ == "__main__":
    asyncio.run(retrieve_data())

