import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone, timedelta
import pytz
import time
from influxdb import InfluxDBClient
import threading
import json

# GET TIME FROM FILE
def get_modification_time(input_path):
    # Get the modification time of the input image file
    modification_time = os.path.getmtime(input_path)
    utc_time = datetime.utcfromtimestamp(modification_time)
    # Format the Chicago time
    chicago_timezone = pytz.timezone('America/Chicago')
    chicago_time = utc_time.replace(tzinfo=timezone.utc).astimezone(chicago_timezone)
    return chicago_time.strftime("%m-%d-%Y %H:%M:%S")

# ADD TIMESTAMP ON TOP OF THE PNG FILE
def add_timestamp_to_image(input_path, output_path):
    # Load the image
    img = plt.imread(input_path)
    # Get creation time of the input image file
    creation_time = get_modification_time(input_path)
    # Add timestamp to the image
    plt.imshow(img)
    plt.text(10, -150, f'Modified at: {creation_time}', color='white', fontsize=12,
             bbox=dict(facecolor='black', alpha=0.7), verticalalignment='top')
    # Remove axis
    plt.axis('off')
    # Save the modified image
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

# EXECUTE CONTINUOUS PLOT TRANSFERING
def main():

    # Iterate over each file in the directory
    directory = "/home/nfs/minerva/dqmtest_cpernas/SL7_testing/gmbrowser/plots/"

    # Log entry file
    log_entry_file = "/home/nfs/minerva/Mx2_monitoring/last_log_entry.txt"

    # Source InfluxDB connection settings
    source_host = '192.168.197.46'
    source_port = 8086

    # Connect to the source InfluxDB instance
    source_client = InfluxDBClient(source_host, source_port, "mx2_logs")
    source_client.create_database("mx2_logs")
    source_client.switch_database("mx2_logs")

    while True:
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                # Input and output paths for each file
                input_path = os.path.join(directory, filename)
                output_path = os.path.join("/data/grafana/Mx2/", os.path.basename(input_path))
                
                # Add timestamp to the image
                add_timestamp_to_image(input_path, output_path)
        
        # Add timestamp to the image
        add_timestamp_to_image(input_path, output_path)

        # Read JSON line from file
        log_entry_file = "/home/nfs/minerva/Mx2_monitoring/last_log_entry.txt"
        with open(log_entry_file, 'r') as file:
            json_line = file.readline().strip()
        data = json.loads(json_line)

        # Extract elements
        subrun_number = data['subrun_number']
        run_number = data['run_number']
        message = data['message']
        message_type = data['type']
        daq_status = data['DAQ_status']
        mode = data['mode']
        DAQ_summary_log = data['DAQ_summary_log']

        # Define data point
        data_point = {
            "measurement": "logs",
            "time": datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
            "fields": {
                "run_number": int(run_number),
                "subrun_number": int(subrun_number),
                "type": message_type,
                "message": message,
                "daq_status" : daq_status,
                "daq_summary_log" : DAQ_summary_log,
                "mode" : mode
            }
        }

        # Write data point to InfluxDB
        source_client.write_points([data_point])

        # Sleep for 10 seconds
        time.sleep(10)

# EXECUTE CONTINUOUS LOG READER
if __name__ == "__main__":
    threading.Thread(target=main).start()