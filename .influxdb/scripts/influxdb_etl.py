import requests
from influxdb import InfluxDBClient
import datetime

# Source InfluxDB connection settings
source_host = 'localhost'
source_port = 8086

# Target InfluxDB connection settings
target_host = 'localhost'
target_port = 18086

# Connect to the source InfluxDB instance
source_client = InfluxDBClient(host=source_host, port=source_port)

# Connect to the target InfluxDB instance
target_client = InfluxDBClient(host=target_host, port=target_port)

# Get list of databases in the source InfluxDB
databases = source_client.get_list_database()

for db in databases:
    #if db['name'] != '_internal': 
    if db['name'] != '_internal' and db['name'] != 'gizmo' and 'module' not in db['name']:  
        source_client.switch_database(db['name'])
        measurements = source_client.get_list_measurements()
        target_client.create_database(db['name'])
        target_client.switch_database(db['name'])
        print(measurements)
        for measurement in measurements:
            measurement_name = measurement['name']

            #Query data from the measurement
            query = f'SELECT * FROM "{measurement_name}"'
            
            result = source_client.query(query)
            # Get the points from the result
            points = list(result.get_points())

            # Write data to the target database
            for point in points:
                
                # Initializing and filling data dictionaries
                float_dict = {}
                str_dict = {}
                time = point['time']
                point.pop('time')
                for key, value in point.items():
                    if isinstance(value, float):
                        float_dict[key] = value
                    elif isinstance(value, str):
                        str_dict[key] = value
 
                time_object = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_time = time_object.strftime("%Y%m%d %H:%M:%S")

                target_client.write_points([{
                    "measurement" : measurement_name,
                    "time" : formatted_time,
                    "tags" : str_dict,
                    "fields" : float_dict
                }])
                
target_client.close()
source_client.close()

print("Data transfer completed.")


#push_to_db("gizmo", "phase")

def push_to_db(db_name, measurement):

    source_db = db_name

    target_db = db_name

    # Query to select data from the source database
    query = 'SELECT * FROM ' + measurement

    # Switch to current database
    target_client.switch_database(db_name)

    # Query data from the source database
    result = source_client.query(query, database=source_db)

    # Get the points from the result
    points = list(result.get_points())

    # Write data to the target database
    for point in points:
        # Modify the point if necessary (e.g., change measurement name)
        #iso_timestamp = point['time']
        #iso_datetime = datetime.datetime.fromisoformat(iso_timestamp[:-1]) 
        #unix_timestamp_ns = int(iso_datetime.timestamp()) * 1_000_000_000
        #point['time'] = unix_timestamp_ns

        json_payload = []
        data = {
            "measurement" : measurement,
            "time" : point['time'],
            "fields" : {
                "phase" : point[measurement]
                }
        }
        json_payload.append(data)
        # Write the point to the target database
        target_client.write_points(json_payload)

    target_client.close()
    source_client.close()

    print("Data transfer completed: " + db_name + " " + measurement)
